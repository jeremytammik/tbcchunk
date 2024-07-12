# tbcchunk

Chunk The Building Coder blog posts for LLM RAG.

Python code generated by [Claude](https://claude.ai/).

I asked claude.ai to chunk The Building Coder blog posts for LLM RAG with the following series of prompts:

- how would you suggest chunking this markdown-formatted blog post, splitting it up into separate documents delineated by the #### h4 section headers?
- that sounds good. how would you handle the same task automatically for 2046 blog posts?
- could you suggest how to code this in Python, please?
- actually, please improve the script as follows: split the input MD files into chunks using all headers as separators, and store the output in JSON files. each JSON should contain the following fields: original filename, header text, local header href, and chunk text.
- the script you provided misses many of the section headers, because they have a href html tag directly joined to the markup header hash characters, like this: ####<a name=\"2\"></a> Personalised Material Asset Properties
- it generated 696 json files, one for each blog posts from number 1351 to today's number 2046.

The earlier blog posts until number 1350 were written in HTML, so they require a different script for chunking.

The result looks perfect.

I corrected nothing whatsoever, didn't even look at the code generated.
All I did was type in the input and output folder paths.

I went on to ask for a similar script to process earlier html-formatted blog posts, using the following prompts:

- that worked very well, and the result looks good. i also have a collection of older blog posts that i wrote in html instead of markdown. could you please write a similar script to chunk up the html blog posts in a similar way to the same json format?
- that script worked fine for a few of the files, but then it produced the following error: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 4049: invalid continuation byte
- i'm afraid that made things worse. now it produces an error in the very first file, saying: File "/Users/jta/a/src/python/tbcchunk/tbcchunk3.py", line 34, in chunk_html: `for elem in soup.body.children`: AttributeError: 'NoneType' object has no attribute 'children'

After that, all was well, all 2046 blog posts processed and chunked.
