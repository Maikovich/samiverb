<?php
namespace SamiverbBundle\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolverInterface;

class VerbValidateType extends AbstractType
{
	public function buildForm(FormBuilderInterface $builder, array $options)
	{
		$builder
			->add('verb', 'text')
			->add('email', 'email')
		;
	}

	public function setDefaultOptions(OptionsResolverInterface $resolver)
	{
		$resolver->setDefaults(array(
			'data_class' => 'SamiverbBundle\Entity\VerbValidate',
			'csrf_protection' => true,
      'csrf_field_name' => '_token',
      // a unique key to help generate the secret token
      'intention'       => '_verb_validate',
		));
	}

	public function getName()
	{
		return 'verbValidate';
	}
}