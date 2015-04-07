<?php

namespace SamiverbBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use JMS\Serializer\SerializerBuilder;
use SamiverbBundle\Entity\Verb;
use SamiverbBundle\Entity\VerbDirectory;
use SamiverbBundle\Entity\VerbRequest;
use SamiverbBundle\Entity\Special\CrsfAttack;

use Symfony\Component\Form\Extension\Csrf\CsrfProvider\CsrfProviderInterface;

class APIController extends Controller
{

  private function JSONResponse($content)
  {
    // make the response
    $response = new Response();
    $response->setContent($content);
    $response->headers->set('Content-Type', 'application/json');
    $response->headers->set('charset', 'utf-8');

    return $response;
  }

  private function flushCrsfAttack($remote_addr, $http_x_forwarded_for)
  {
    $crsf = new CrsfAttack();
    
    $crsf->setRemoteAddress($remote_addr);
    $crsf->setHttpXForwardedFor($http_x_forwarded_for);
    $crsf->setDate();

    $em = $this->getDoctrine()->getManager();
    
    $em->persist($crsf);
    $em->flush();

    return $this;
  }

  /**
   * @Route("/crsf/{mode}",
   *  name="crsf-generate"
   * )
   */
  public function crsfGenerateAction($mode)
  {
    if ($mode < 1 || $mode > 2) {
      return new Response($mode, 404, 
      array('Content-Type' => 'text/plain'));
    }

    $token = $this->get('security.csrf.token_manager')->refreshToken('_validate_verb_mode_'.$mode);

    return new Response($token, 
      200, array('Content-Type' => 'text/plain'));
  }

  /**
   * @Route("/request/{verb}",
   *  name = "request-verb"
   *  )
   */
  public function requestVerbAction($verb)
  {
    $verbObj = new Verb($verb);

    if (!$verbObj->checkVerb()) {
      return new Response($verbObj->getVerb(), 404, 
      array('Content-Type' => 'text/plain'));
    }

    $dirObj = new VerbDirectory('bundles/samiverb/json', 'json');
    $invldDirObj = new VerbDirectory('bundles/samiverb/json/invalid', 'json');

    // process verb, if something went wrong, send bad response
    $rVal = $verbObj->processVerb(
      $dirObj->listValidVerbs(),
      $invldDirObj->listInvalidVerbs()
    );

    if ($rVal == -1) {
      return new Response($verbObj->getVerb(), 404, 
      array('Content-Type' => 'text/plain'));
    }
    else if ($rVal == 5) {
      // update metadata
      $invldDirObj->updateMetadata($verbObj->getVerb(), 2);
      // fetch the json
      $jsonContents = file_get_contents(
        $invldDirObj->getVerbPath($verbObj->getVerb()));
    }
    else {
      // update metadata
      $dirObj->updateMetadata($verbObj->getVerb(), $rVal);
      // fetch the json
      $jsonContents = file_get_contents(
        $dirObj->getVerbPath($verbObj->getVerb()));
    }

    return $this->JSONResponse($jsonContents);
  }

  /**
   * @Route("/suggestions/{verb}",
   *  name = "suggestions-verb"
   *  )
   */
  public function suggestionsVerbAction($verb)
  {
    $vldDir = new VerbDirectory('bundles/samiverb/json', 'json');
    
    $verbObj = new Verb($verb);

    if (!$verbObj->checkVerb()) {
      return new Response($verbObj->getVerb(), 404, 
      array('Content-Type' => 'text/plain'));
    }
    
    $res = array();
    $res['matches'] = $vldDir->listClosestMatches($verbObj->getVerb());

    $encode_opts = JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT;
    $jsonContents = json_encode($res, $encode_opts);

    return $this->JSONResponse($jsonContents);
  }

  /**
   * @Route("/validate",
   *  name = "validate"
   *  )
   */
  public function validateVerbAction(Request $request)
  {
    // fetch data from request
    $data = $request->getContent();
    
    // initialize JMS serializer      
    $serializer = SerializerBuilder::create()->build();

    $verbRequest = $serializer->deserialize($data, 'SamiverbBundle\Entity\VerbRequest', 'json');
    
    // set date
    $verbRequest->setDate();

    // validate input
    $validator = $this->get('validator');
    $errors = $validator->validate($verbRequest);

    if (count($errors) > 0) {
      $errorsString = (string) $errors;

      //return new Response($errorsString, 400,
       // array('Content-Type' => 'text/plain'));
    }

    // check csrf_token
    if ( !($this->isCsrfTokenValid( '_validate_verb_mode_'.$verbRequest->getMode(),
          $request->headers->get('X-CSRF-Token'))) ) {
      
      // flush CSRF attack to database!
      $remote_addr = $_SERVER['REMOTE_ADDR'];

      if (empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $this->flushCrsfAttack($remote_addr, "");
      } else {
        $this->flushCrsfAttack($remote_addr, $_SERVER['HTTP_X_FORWARDED_FOR']);
      }

      return new Response("Not Found", 400,
        array('Content-Type' => 'text/plain'));
    }

    // persist and flush to verb request to database
    $em = $this->getDoctrine()->getManager();
    
    $repository = $em->getRepository('SamiverbBundle:VerbRequest');

    $query = $repository->createQueryBuilder('r')
      ->where('r.verb = :verb AND r.email = :email')
      ->setParameter('verb', $verbRequest->getVerb())
      ->setParameter('email', $verbRequest->getEmail())
      ->getQuery();

    $req = $query->getResult();

    // only persist if the request hasn't been made before
    // with the same email address
    if (count($req) === 0) {

      $em->persist($verbRequest);
      $em->flush();
    
    }

    return new Response('Created verb request id '.$verbRequest->getId(), 
      200, array('Content-Type' => 'text/plain'));
  }

}
