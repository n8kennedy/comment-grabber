Comment Grabber
Nate Kennedy
2013-10-18
==

python script to print comments found in a code file.

==
usage:
$ grab file[ file2...]

$ grab file.js
> file.js
> /*
>   wrapped comment
> */
> var inline = comment; // inline comments

$ grab --type=html index.html
> index.html
> <!--
>   open comment block
> -->
> <a href="#">inline</a> <!-- some inline comment -->

==
options: (would be nice to have)

  --lang=language   specicy the language to check for
                    languages include: {
                      python (py),
                      javascript (js),
                      html,
                      c#
                    }

  -n, --line-num    print line numbers

==

