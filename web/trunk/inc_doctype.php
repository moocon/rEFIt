<?php
// $Id$

$self = $_SERVER['PHP_SELF'];
$selfname = substr($self, strrpos($self, "/") + 1);

// determine section and page
$section = "main";
if (substr($self, 0, 6) == "/info/")
  $section = "info";
if (substr($self, 0, 5) == "/doc/")
  $section = "doc";
$index_html = 0;
if ($selfname == "index.html")
  $index_html = 1;

// Documentation section: automatic "next" and "up" links
if ($section == "doc") {
  include "inc_docmap.php";
  if ($index_html) {
    $nextdocpage = $docmap[0];
  } else {
    $doccount = count($docmap);
    for ($i = 0; $i < $doccount; $i++) {
      if ($docmap[$i][0] == $selfname) {
        if ($i > 0)
          $prevdocpage = $docmap[$i - 1];
        if ($i + 1 < $doccount)
          $nextdocpage = $docmap[$i + 1];
      }
    }
  }
}

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
