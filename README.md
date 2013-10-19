Comment Grabber
====

A simple python script to grep comments from code files.

installation:
----

> $ python setup.py install

usage:
----

> $ comments file[ file2...]

> $ comments file.js  
>  file.js  
>  /*  
>    wrapped comment  
>  */  
>  var inline = comment; // inline comments  

> $ comments --type=html index.html  
>  index.html  
>  <!--  
>    open comment block  
>  -->  
>  <a href="#">inline</a> <!-- some inline comment -->  
