A while ago, I failed to find an appropriate tool for making sure no files were lost during file structure restructuring, so I built my own lightweight CLI tool in python. Today I decided to publish it here because... it deserves to be accessible from every computer.
# Usage
```alreadyexists [path]``` Generates MD5 hashes for all files recursively under \<path>. You will be prompted to either save the hashes to a \<path>/.hashes file or display them directly in the terminal.

```alreadyexists [path1] [path2/file]``` Compares files recursively under <path1> against those under \<path2> or a previously saved .hashes \<file>. It reports any missing or un-matched files whose MD5 hashes were not found recursively under the \<path2>.
