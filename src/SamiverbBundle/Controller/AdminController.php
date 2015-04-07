<?php

namespace SamiverbBundle\Controller;
use SamiverbBundle\Controller\MainController;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Security;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use JMS\Serializer\SerializerBuilder;
use SamiverbBundle\Entity\Verb;
use SamiverbBundle\Entity\VerbDirectory;
use SamiverbBundle\Entity\VerbRequest;

class AdminController extends MainController
{

  /**
   * Moves and returns a list of invalid verbs
   *
   * @param (array) $verb || (string) $verb
   * @return (array) $resList
   */
  private function moveAndListInvalidVerbs($verb = false)
  {
    $vldDir = new VerbDirectory('bundles/samiverb/json', 'json');
    $invldDir = new VerbDirectory('bundles/samiverb/json/invalid', 'json');

    if ($verb == false) {
      
      $resList = $vldDir->listBadVerbs($vldDir->listInvalidVerbs());
    
    }
    else {

      $verbObj = new Verb($verb);

      if (!$verbObj->checkVerb()) {
        return new Response($verbObj->getVerb(), 404, 
        array('Content-Type' => 'text/plain'));
      }

      $resList = $vldDir->listBadVerbs($verbObj->getVerb());

    }

    if (!empty($resList)) {
      // move from valid directory to invalid
      $vldDir->moveVerbs($resList, $invldDir);
    }

    return $resList;
  }

  /**
   * Sends a notification email about verb validation
   *
   * @param VerbRequest $request, (string) $sendTo
   * @return bool
   */
  private function sendVerbNotificationEmail(VerbRequest $request, $sendTo)
  {
    $mailer = $this->get('mailer');
    $message = $mailer->createMessage()
        ->setSubject('Thanks for your contribution!')
        ->setFrom('noreply@samiverb.com')
        ->setTo($sendTo)
        ->setBody(
            $this->renderView(
                'SamiverbBundle::Emails/validation.html.twig',
                array(
                  'verb' => $request->getVerb(),
                  'date' => $request->getDate()
                )
            ),
            'text/html'
        )
    ;
    return $mailer->send($message);
  }

  /**
   * @Route("/panel", name="_admin_panel")
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function panelAction(Request $request)
  {
    return $this->backEndController($request,
      'SamiverbBundle::admin/panel.html.twig', array(
        'activeTab' => 'panel'
        )
    );
  }

  /**
   * @Route("/panel/requests", name="_admin_requests")
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function requestsAction(Request $request)
  {
    $requests = $this->getDoctrine()
        ->getRepository('SamiverbBundle:VerbRequest')
        ->findAll();

    return $this->backEndController($request,
      'SamiverbBundle::admin/requests.html.twig', array(
        'activeTab' => 'requests',
        'requests' => $requests
        )
    );
  }

  /**
   * @Route("/panel/request/validate/{id}", 
   *  name="_admin_request_validate",
   *  defaults={"id"=0}
   * )
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function requestValidateAction($id)
  {
    if ($id > 0) {

      $em = $this->getDoctrine()->getManager();
      $repository = $em->getRepository('SamiverbBundle:VerbRequest');

      $request = $repository->find($id);

      if (!$request) {
        throw $this->createNotFoundException(
            'No request found for id '.$id
        );
      }

      // move and list potential invalid verb
      $isInvalid =  $this->moveAndListInvalidVerbs($request->getVerb());

      // find all requests bound to the verb
      $requests = $repository->findByVerb($request->getVerb());

      if (empty($isInvalid)) {
        // send notification if the verb was valid := empty list

        foreach ($requests as $req) {
          $sendTo = $req->getEmail();
          
          // send notification
          $this->sendVerbNotificationEmail($req, $sendTo);

          // remove the request
          $em->remove($req);
        }

      }
      else {
        // invalid verb
            
        foreach ($requests as $req) {
          $em->remove($req);
        }
      }

      $em->flush();
    }

    return $this->redirectToRoute('_admin_requests');
  }

  /**
   * @Route("/panel/request/delete/{id}", 
   *  name="_admin_request_delete",
   *  defaults={"id"=0}
   * )
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function requestDeleteAction($id)
  {
    if ($id > 0) {

      $em = $this->getDoctrine()->getManager();
      $repository = $em->getRepository('SamiverbBundle:VerbRequest');

      $request = $repository->find($id);

      if (!$request) {
        throw $this->createNotFoundException(
            'No request found for id '.$id
        );
      }

      $requests = $repository->findByVerb($request->getVerb());

      foreach ($requests as $req) {
        $em->remove($req);
      }

      $em->flush();
    }

    return $this->redirectToRoute('_admin_requests');
  }

  /**
   * @Route("/panel/threat/block/{id}", 
   *  name="_admin_threat_block",
   *  defaults={"id"=0}
   * )
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function blockThreatAction($id)
  {
    if ($id > 0) {

      $em = $this->getDoctrine()->getManager();
      $repository = $em->getRepository('SamiverbBundle:Special\CrsfAttack');

      $attack = $repository->find($id);

      if (!$attack) {
        throw $this->createNotFoundException(
            'No attack found for id '.$id
        );
      }
      
    }

    return $this->redirectToRoute('_admin_requests');
  }

  /**
   * @Route("/panel/threat/delete/{id}", 
   *  name="_admin_threat_delete",
   *  defaults={"id"=0}
   * )
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function threatDeleteAction($id)
  {
    if ($id > 0) {

      $em = $this->getDoctrine()->getManager();
      $repository = $em->getRepository('SamiverbBundle:Special\CrsfAttack');

      $attack = $repository->find($id);

      if (!$attack) {
        throw $this->createNotFoundException(
            'No attack found for id '.$id
        );
      }

      // remove threat
      $em->remove($attack);
      $em->flush();
      
    }

    return $this->redirectToRoute('_admin_threats');
  }

  /**
   * @Route("/panel/threats", name="_admin_threats")
   *
   * @Security("has_role('ROLE_ADMIN')")
   */
  public function threatsAction(Request $request)
  {
    $attacks = $this->getDoctrine()
        ->getRepository('SamiverbBundle:Special\CrsfAttack')
        ->findAll();

    return $this->backEndController($request,
      'SamiverbBundle::admin/threats.html.twig', array(
        'activeTab' => 'threats',
        'attacks' => $attacks
        )
    );
  }


}