<?php
namespace SamiverbBundle\Entity;

use JMS\Serializer\Annotation\Type;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\Context\ExecutionContextInterface;
use SamiverbBundle\Entity\Verb;
use SamiverbBundle\Entity\VerbDirectory;

use Doctrine\ORM\Mapping as ORM;

/**
 * Entity for requesting validation 
 * of verbs
 *
 * @ORM\Entity
 * @ORM\Table(name="verbrequest")
 */
class VerbRequest
{
  /**
   * @ORM\Column(type="integer")
   * @ORM\Id
   * @ORM\GeneratedValue(strategy="AUTO")
   */
  protected $id;

  /**
   * @ORM\Column(type="string", length=100)
   *
   * @Assert\Length(
   *  min = 4,
   *  max = 100
   * )
   *
   * @Type("string")
   */
  protected $verb;
  
  /**
   * @ORM\Column(type="string", length=100)
   *
   * @Assert\Length(
   *  min = 2,
   *  max = 100
   * )
   * @Assert\Email(
   *    checkMX = true
   * )
   *
   * @Type("string")
   */
  protected $email;
  
  /**
   * @ORM\Column(type="integer")
   *
   * @Assert\Range(
   *    min = 1,
   *    max = 2
   * )
   *
   * @Type("integer")
   */
  protected $mode;


  /**
   * @ORM\Column(type="datetime")
   */
  protected $date;

  /**
   * Validate email
   * Callback for validator service
   *
   * @Assert\Callback
   */
  public function validateEmail(ExecutionContextInterface $context)
  {
    if ( !(filter_var($this->getEmail(), FILTER_VALIDATE_EMAIL)) ) 
    {
      $context->buildViolation('Email not valid (filter validate email).')
        ->atPath('email')
        ->addViolation();
    }
  }

  /**
   * Validate verb
   * Callback for validator service
   *
   * @Assert\Callback
   */
  public function validateVerb(ExecutionContextInterface $context)
  {
    // fetch directories
    if ($this->getMode() == 1) {
      $dir = new VerbDirectory('bundles/samiverb/json', 'json');
    } else {
      $dir = new VerbDirectory('bundles/samiverb/json/invalid', 'json');
    }

    // fetch verb object
    $verbObj = $this->getVerbObj();

    if ( !($verbObj->exists($dir->listInvalidVerbs())) )
    {
      $context->buildViolation('Verb has not been processed in mode '. 
        (string) $this->getMode())
        ->atPath('verb')
        ->addViolation();
    }
  }

  /**
   * Get verb object
   *
   * @return Verb
   */
  public function getVerbObj() 
  {
    return new Verb($this->getVerb());
  }

    /**
     * Get id
     *
     * @return integer 
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Set verb
     *
     * @param string $verb
     * @return VerbRequest
     */
    public function setVerb($verb)
    {
        $this->verb = $verb;

        return $this;
    }

    /**
     * Get verb
     *
     * @return string 
     */
    public function getVerb()
    {
        return $this->verb;
    }

    /**
     * Set email
     *
     * @param string $email
     * @return VerbRequest
     */
    public function setEmail($email)
    {
        $this->email = $email;

        return $this;
    }

    /**
     * Get email
     *
     * @return string 
     */
    public function getEmail()
    {
        return $this->email;
    }

    /**
     * Set date (now)
     *
     * @param \DateTime $date
     * @return VerbRequest
     */
    public function setDate()
    {
        $this->date = new \DateTime("now");

        return $this;
    }

    /**
     * Get date
     *
     * @return \DateTime 
     */
    public function getDate()
    {
        return $this->date;
    }

    /**
     * Set mode
     *
     * @param integer $mode
     * @return VerbRequest
     */
    public function setMode($mode)
    {
        $this->mode = $mode;

        return $this;
    }

    /**
     * Get mode
     *
     * @return integer 
     */
    public function getMode()
    {
        return $this->mode;
    }
}
