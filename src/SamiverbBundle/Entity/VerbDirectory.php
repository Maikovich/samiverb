<?php
namespace SamiverbBundle\Entity;

class VerbDirectory {
  protected $dir;
  protected $formatExt;
  protected $metadataFile;


  /* PRIVATE FUNCTIONS */

  public function __construct($dir, $format)
  {
    $this->dir = $dir;
    $this->formatExt = $format;
    $this->metadataFile = 'info.json';
  }

  private function getMetaDataPath()
  {
    return $this->dir.'/'.$this->metadataFile;
  }

  private function loadJSONtoArray($filename)
  {
    $contents = file_get_contents($filename);

    return json_decode($contents, true);
  }

  private function writeJSONtoFile($filename, $obj)
  {
    $f = fopen($filename, 'w');
    $encode_opts = JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT;
    fwrite($f, json_encode($obj, $encode_opts));
    fclose($f);
  }

  private function loadMetadata()
  {
    return $this->loadJSONtoArray($this->getMetaDataPath());
  }

  private function writeMetadata($new)
  {
    $this->writeJSONtoFile($this->getMetaDataPath(), $new);
  }
  
	private function listVerbs($valid = 1) 
	{
    $verbs = array();
    $i = 0;

    $metadataObj = $this->loadMetadata();

    foreach ($metadataObj['verbs'] as $vObj) {
      if ($vObj['valid'] != $valid) {
        continue;
      }
      array_push($verbs, $vObj['name']);
    }

    return $verbs;
	}

  private function removeVerb($verb)
  {
    return unlink($this->getVerbPath($verb));
  }

  private function removeVerbs($verbs)
  {
    foreach ($verbs as $verb) {
      if ($this->removeVerb($verb) == false) {
        return false;
      }
    }
    return true;
  }

  /* http://php.net/manual/en/function.levenshtein.php */
  //
      private function utf8_to_extended_ascii($str, &$map)
      {
        // find all multibyte characters (cf. utf-8 encoding specs)
        $matches = array();
        if (!preg_match_all('/[\xC0-\xF7][\x80-\xBF]+/', $str, $matches))
            return $str; // plain ascii string
       
        // update the encoding map with the characters not already met
        foreach ($matches[0] as $mbc)
            if (!isset($map[$mbc]))
                $map[$mbc] = chr(128 + count($map));
       
        // finally remap non-ascii characters
        return strtr($str, $map);
      }

  //
  /* ///////                                             */

  /* PUBLIC FUNCTIONS */

  public function getVerbPath($verb)
  {
    return $this->dir.'/'.$verb.'.'.$this->formatExt;
  }

  public function getDirName()
  {
    return $this->dir;
  }

  public function removeTags($var)
  {
    $type = gettype($var);
    if ($type == "string") {
      return preg_replace("/\\.[^.\\s]{3,4}$/", "", $var);
    }
    else if ($type == "array") {
      $new = array();
      foreach ($var as $e) {
        array_push($new, preg_replace("/\\.[^.\\s]{3,4}$/", "", $e));
      }
      return $new;
    }
    else { return false; }
  }

  public function listClosestMatches($verb)
  {
    $vldVerbs = $this->listValidVerbs();

    $matches = array();
    $stack = array();
    $shortest = -1;
    
    $charMap = array();
    $eVerb = $this->utf8_to_extended_ascii($verb, $charMap);

    shuffle($vldVerbs);
    foreach ($vldVerbs as $vldVerb) {
      $eVldVerb = $this->utf8_to_extended_ascii($vldVerb, $charMap);
      $lev = levenshtein($eVerb, $eVldVerb);

      if ($lev <= $shortest || $shortest < 0) {
        $closest = $vldVerb;
        $shortest = $lev;
        array_push($stack, array("verb" => $closest, "dist" => $shortest));
      }
    }

    while (1) {
      $res = array_pop($stack);

      if ($res['dist'] > $shortest) {
        break;
      }
      else {
        array_push($matches, $res['verb']);
      }
    }
    
    return $matches;
  }

  public function listBadVerbs($verbs)
  {
    $badVerbs = array();
    
    if (gettype($verbs) == "string") {
      $verbs = array($verbs);
    }
    else {
      if (gettype($verbs) != "array")
        return false;
    }
    
    foreach ($verbs as $v) {
      // look up in the metadata
      $vObj = $this->readMetadataVerb($v);

      if ($vObj == false) {
        // verb does not even exist
        continue;
      }
      // if it is already checked, go to next verb
      if ($vObj['valid'] == 1) {
        continue;
      }
      
      // create a stream
      $opts = array(
        'http' => array (
          'method' => 'GET'
        )
      );

      $context = stream_context_create($opts);

      $fileContents = file_get_contents(
        'http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text='.$v.'&pos=Any&mode=minimal&action=paradigm&charset=utf-8&lang=sme&plang=sme',
        false, 
        $context
      );

      $checkStr = '<font color="white">'.$v.'</font>';
      
      $jsonObj = $this->loadJSONtoArray($this->getVerbPath($v));
      // correct verb, edit json file
      $jsonObj['check'] = 1;


      if (strpos($fileContents, $checkStr) === false) {
        // false verb, append to bad list
        $jsonObj['valid'] = 0;

        array_push($badVerbs, $v);
      }
      else {
        $jsonObj['valid'] = 1;
        // update metadata
        $this->updateMetadata($v, 4);
      }
      
      // write new json to file
      $this->writeJSONtoFile($this->getVerbPath($v), $jsonObj);
    
    }
    return $badVerbs;
  }

  public function readMetadataVerb($verb) {
    $metadataObj = $this->loadMetadata();

    foreach ($metadataObj['verbs'] as $vObj) {
      if ($vObj['name'] != $verb) {
        continue;
      }
      return $vObj;
    }
    return false;
  }

  public function updateMetadata($verb, $type, $tmsAcsd = 1)
  {
    // fetch metadata
    $metadataObj = $this->loadMetadata();

    if ($type == 1) {      // create
    
      foreach ($metadataObj['verbs'] as $vObj) {
        
        if ($vObj['name'] == $verb) {
          return;
        }
      }

      $metadataObj['count'] ++;

      array_push(
        $metadataObj['verbs'], 
        array('name' => $verb,
              'valid' => 0,
              'timesAccessed' => $tmsAcsd, 
              'lastAccessed' => date("Y-m-d H:i:s")
             )
      );
    }
    else if ($type == 2) {  // update

      foreach ($metadataObj['verbs'] as $idx => $vObj) {
        
        if ($vObj['name'] == $verb) {
          break;
        }
      }

      if ($vObj['name'] != $verb) {
        return;
      }

      $metadataObj['verbs'][$idx]['timesAccessed'] ++;
      $metadataObj['verbs'][$idx]['lastAccessed'] = date("Y-m-d H:i:s");
    }
    else if ($type == 3) {  // delete

      foreach ($metadataObj['verbs'] as $idx => $vObj) {
        
        if ($vObj['name'] == $verb) {
          break;
        }
      }

      if ($vObj['name'] != $verb) {
        return;
      }
      
      unset($metadataObj['verbs'][$idx]);
      $metadataObj['count'] --;

    }
    else if ($type == 4) {  // validated

      foreach ($metadataObj['verbs'] as $idx => $vObj) {
        
        if ($vObj['name'] == $verb) {
          break;
        }
      }

      if ($vObj['name'] != $verb) {
        return;
      }

      $metadataObj['verbs'][$idx]['valid'] = 1;
    }
    else {
      return false;
    }

    $this->writeMetadata($metadataObj);
  }

  public function moveVerbs($verbs, $otherDir) 
  {
    if (gettype($verbs) == "string") {
      $verbs = array($verbs);
    }
    else {
      if (gettype($verbs) != "array")
        return false;
    }

    foreach ($verbs as $v) {
      
      // read metadata verb object
      $vObj = $this->readMetadataVerb($v);

      // remove the old metadata
      $this->updateMetadata($v, 3);

      // copy the file to the other verb directory
      if (!copy($this->getVerbPath($v), $otherDir->getVerbPath($v))) {
        echo "failed to copy $file \n";
        continue;
      }

      // create new verb in metadata
      $otherDir->updateMetadata($v, 1, $vObj['timesAccessed']);

      // remove the file in the current verb directory
      $this->removeVerb($v);

    }

    return true;
  }

  public function listValidVerbs()
  {
    return $this->listVerbs($valid = 1);
  }

  public function listInvalidVerbs()
  {
    return $this->listVerbs($valid = 0);
  }

}