Introduction:
	> Compression is usually done for either saving space on a disk or speed up data transfer time
	> Two main forms of compression:
					1. Lossy: Where by compression you lose some info. Ex: MP3
					2. Lossless: The file gets smaller and the original file is still
					   retrievable. Ex: FLAC
	> In this project we'll be working with the lossless kind called Huffman.
	> Computes store data by mapping them out toa set of {1,2}
	> If we were to assing data to a certain number of bits, every element would have 2 bits, and thus
	  aaaa would have 8 bits
	> but if we were to drop that requirement of same lenght, we would have 4 for aaaa, if we were to
	  asign a to 1
	> However this can be ambiguous and thus a certain piece of code can represent multipule things
 	> Thus we can decode each letter to a very different code and thus no ambiguity 
	> We need to use the best code to make the shortest letters
	> The prefix code for a file is the one that is the shorttest
	> Or maximises the amount of file we can compress
	> The huffman algorithem is one where we have a tree of symbols and the code for each symbol can
	 can be figured out by tracing it from the root and adding a 0 for left turns and 1 for rights
