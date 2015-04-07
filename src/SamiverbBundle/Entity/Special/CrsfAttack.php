<?php
namespace SamiverbBundle\Entity\Special;

use JMS\Serializer\Annotation\Type;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\Context\ExecutionContextInterface;

use Doctrine\ORM\Mapping as ORM;

/**
 * Entity for CRSF attack instances 
 *
 * @ORM\Entity
 * @ORM\Table(name="crsfattack")
 */
class CrsfAttack
{

  /**
   * @ORM\Column(type="integer")
   * @ORM\Id
   * @ORM\GeneratedValue(strategy="AUTO")
   */
  protected $id;

  /**
   * @ORM\Column(type="string", length=45)
   *
   * @Assert\Ip(version="all")
   *
   * @Type("string")
   */
  protected $remoteAddress;

  /**
   * @ORM\Column(type="string", length=45)
   *
   * @Type("string")
   */
  protected $httpXForwardedFor;

  /**
   * @ORM\Column(type="datetime")
   */
  protected $date;

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
   * Set remoteAddress
   *
   * @param string $remoteAddress
   * @return CrsfAttack
   */
  public function setRemoteAddress($remoteAddress)
  {
      $this->remoteAddress = $remoteAddress;

      return $this;
  }

  /**
   * Get remoteAddress
   *
   * @return string 
   */
  public function getRemoteAddress()
  {
      return $this->remoteAddress;
  }

  /**
   * Set httpXForwardedFor
   *
   * @param string $httpXForwardedFor
   * @return CrsfAttack
   */
  public function setHttpXForwardedFor($httpXForwardedFor)
  {
      $this->httpXForwardedFor = $httpXForwardedFor;

      return $this;
  }

  /**
   * Get httpXForwardedFor
   *
   * @return string 
   */
  public function getHttpXForwardedFor()
  {
      return $this->httpXForwardedFor;
  }

}
