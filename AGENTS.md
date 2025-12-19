Repository is meant to experiment with development of games using python and its libraries such as Pygame.  
Repository may contain multiple different projects/games.  
Ideally, the structure of packages should be such that generally useful modules are in a package from which can borrow individual projects some bits and pieces.  
Each individual project/game should have its own package with modules related only to the particular package. 
Therefore, if we start to develop new game which could use something what was initially exclusive for another game then I expect this part of code to be refactored into the common packages.
However, I hope you to suggest such placing of modules that this refactoring will not be necessary.  
Whole repo will have one shared virtual environment. 
