<?php
namespace SamiverbBundle\Entity;

use Symfony\Component\Validator\Constraints as Assert;

/**
 * Verb entity
 */
class Verb
{
	protected $verb;

	/**
	 * Constructor
	 * 
	 * @param string $verb
	 * @return Verb
	 */
	public function __construct($verb) 
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
	 * Set verb
	 * 
	 * @param string $verb
	 * @return Verb
	 */
	public function setVerb($verb) 
	{ 
		$this->verb = $verb;

		return $this; 
	}

	/**
	 * Checks verbs possibility
	 * 
	 * @return integer (1: success, 0: failure)
	 */
	public function checkVerb()
	{
		// to lowercase
		$this->verb = mb_strtolower($this->verb, 'UTF-8');
		// replace non-sami to sami characters
		$this->replaceNonSamiChar();
		// check if verb makes sense regarding grammar
		if (!$this->isPossible()) {
			return 0; // Is not a possible verb
		}
		return 1;
	}

	/**
	 * Processes verb
	 * Writes JSON data to database
	 * 
	 * @param array $valid, array $invalid
	 * @return integer (-1: error, 1: new verb, 2: existed before, 5: invalid verb)
	 */
	public function processVerb($valid, $invalid)
	{
		// check if verb already is conjugated before
		if (!$this->exists($valid)) {
			if ($this->exists($invalid)) {
				return 5; // Is an invalid verb
			}
			// conjugate the verb
			$resVal = exec("python bundles/samiverb/py/jsonwritesamiverb.py ".
				escapeshellarg($this->verb)
			);
			
			// redirect to error page if bad result
			if (!$resVal) {
				return -1; // Something went wrong
			}

			return 1; // Made a new verb
		}

		return 2; // Existed before
	}

	/**
	 * Checks existance of verb in list
	 * 
	 * @param array $list
	 * @return integer (1: success, 0: failure)
	 */
	public function exists($list)
	{
		if ($list == false) {
			return false;
		}
		return in_array($this->verb, $list);
	}

	/**
	 * Checks possibility of Verb's verb
	 * 
	 * @return integer (1: success, 0: failure)
	 */
	private function isPossible()
	{
		if ((strlen($this->verb) >= 4) &&
			(preg_match("/^[a-zŋčđážšŧ]+$/", $this->verb))
		)
		{ return 1; }
		return 0;
	}

	/**
	 * Replaces non Saami characters with 
	 *  Saami characters
	 */
	private function replaceNonSamiChar()
	{
		$this->verb = str_replace(
			array('n1','c1','d1','a1','z1','s1','t1'),
			array('ŋ', 'č', 'đ', 'á', 'ž', 'š', 'ŧ' ), 
			$this->verb
		);
	}
}