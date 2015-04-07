<?php

namespace SamiverbBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class MainController extends Controller
{

	/**
	 * @Route("/", name="home")
	 */
	public function indexAction(Request $request)
	{
		return $this->backEndController($request,
			'SamiverbBundle::index.html.twig', array(
				'activePage' => 'home'
				)
		);
	}

	/**
	 * @Route("/guide", name="guide")
	 */
	public function guideAction(Request $request)
	{
		return $this->backEndController($request,
			'SamiverbBundle::guide.html.twig', array(
				'activePage' => 'guide'
				)
		);
	}

	/**
	 * @Route("/about", name="about")
	 */
	public function aboutAction(Request $request)
	{
		return $this->backEndController($request,
			'SamiverbBundle::about.html.twig', array(
				'activePage' => 'about'
				)
		);
	}

	/**
	 * @Route("/contact", name="contact")
	 */
	public function contactAction(Request $request)
	{
		return $this->backEndController($request,
			'SamiverbBundle::contact.html.twig', array(
				'activePage' => 'contact'
				)
		);
	}

	protected function backEndController(Request $request, 
		$renderPage, $options = false)
	{

		if ($options != false) {
			foreach ($options as $key => $val) {
				$renderArr[$key] = $val;
			}
		}

		if ($this->isGranted('ROLE_ADMIN')) {
			$renderArr['user'] = $this->getUser()->getUsername();
		}

		return $this->render($renderPage, $renderArr);
	}

}