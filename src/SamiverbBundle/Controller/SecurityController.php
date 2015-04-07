<?php

namespace SamiverbBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Component\HttpFoundation\Request;

class SecurityController extends Controller
{

  /**
   * @Route("/login",
   *  name="login_route"
   * )
   */
  public function loginAction(Request $request)
  {
    // redirect to admin page if already logged in
    if ($this->isGranted('ROLE_ADMIN')) {
      return $this->redirectToRoute('_admin_panel');
    }

    $authenticationUtils = $this->get('security.authentication_utils');

    // get a potential login error
    $error = $authenticationUtils->getLastAuthenticationError();

    // last username entered by the user
    $lastUsername = $authenticationUtils->getLastUsername();

    return $this->render(
      'SamiverbBundle::security/login.html.twig',
      array(
        // last username entered
        'last_username' => $lastUsername,
        'error'         => $error
        )
    );
  }

  /**
   * @Route("/login_check", 
   *  name="login_check"
   * )
   */
  public function loginCheckAction()
  {
    // will not be executed
    // the router will be handled by the security system
  }

}
