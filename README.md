twitterMap
==========
By Yanxi Pan(yp2347) and Cheng Liu(cl3173)

Cloud Project2 Twitter Map 

#Project Structure:

##appProj/ 
The Pycharm IDE project
##script/
The installation script to install all the dependency needed by this project
##test/
Test Script to test a certain function of our project

#Useful links
## Google AppEngine Delopy Version:
- [http://cloudtwittermap.appspot.com/](http://cloudtwittermap.appspot.com/)
## Github Repository(Now it is still private)
- [https://github.com/milannic/twitterMap](https://github.com/milannic/twitterMap)
## Pycharm IDE Official Link
- [http://www.jetbrains.com/pycharm/](http://www.jetbrains.com/pycharm/)

#Project Features:
0 **More than 1GB Twitter Raw Data Collected, due to the limitation of the Google AppEngine Free Account, you can check this when demo time**

1 **We parse every twitter and build a keyword list then store it in the datastore as weel as its created time,location,userName,userId,twitterId and original text**

2 **The scatter plot and heat map**

3 **Dynamic Keyword list is generated from the content of the twitter collected, and we update it every midnight automatically**

4 **Every Midnight, we collect new twitter data automatically**

5 **Those Searches seen before will be stored in the memcache**

6 **Timeline Feature To Show the twitter Treads**

7 **Mobile Interface**
