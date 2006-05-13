<?php

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
<p id="footer">Copyright &copy; 2006 Christoph Pfisterer</p>
