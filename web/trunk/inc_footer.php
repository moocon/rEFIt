<?php
// $Id$

// Documentation section: automatic "next" and "up" links
if ($section == "doc") {
  include "inc_docmap.php";
  if ($index_html) {
    $nextdocpage = $docmap[0];
  } else {
    do {
      $currentpage = current($docmap);
      if ($currentpage[0] == $selfname)
        $nextdocpage = next($docmap);
    } while (next($docmap));
  }
  
  print '<p id="pagelink">';
  if ($nextdocpage) {
    print 'Next: <a href="'.$nextdocpage[0].'">'.$nextdocpage[1].'</a>';
    if (!$index_html)
      print '<br>';
  }
  if (!$index_html)
    print 'Up: <a href="index.html">Contents</a>';
  print '</p>';
}

?>
<div id="footer">
<?php

// Automatic "last changed" info from Subversion
if ($vc_author) {
  if (substr($vc_author,0,1) == "$")
    $vc_author = rtrim(substr($vc_author, 1, -1));
  if (substr($vc_date,0,1) == "$")
    $vc_date = rtrim(substr($vc_date, 1, -1));
  if (ereg("^Author: (.*)$", $vc_author, $r)) {
    $author = $r[1];
  } else {
    $author = "-unknown-";
  }
  if (ereg("^Date: ([0-9]{2,4})[/\-]([0-9]{1,2})[/\-]([0-9]{1,2}) ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})", $vc_date, $r)) {
    $date = gmmktime($r[4], $r[5], $r[6], $r[2], $r[3], $r[1]);
  } else {
    $date = filemtime($_SERVER['PATH_TRANSLATED']);
  }
  print '<p id="vcinfo">Last changed by '.$author.' on '.strftime("%a, %b %d %Y", $date).'</p>';
}

?>
<p id="copyright">Copyright &copy; 2006 Christoph Pfisterer</p>
<div id="footerclear"></div>
</div>
