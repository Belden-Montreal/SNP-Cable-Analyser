two main problems to keep in mind to avoid crashing (will patch eventually)

1- in a "embedding" project, when using the pdfexport module;
 since i have not implemented a way to export the "case" parameter yet, clicking "ok" to export the project in pdf form
 WITHOUT UNCHECKING ALL THE "CASE" PARAMETERS in the parameter list will crash the app.
	-i cant take to option away or the cases wont appear in the program at all, so you need to uncheck the parameter manually

2- when importing an existing project (so after saving a project, it creates a folder with a XML and a folder containing 
all the snps)the crash occurs when you open a projact that has been moved since its creation
	-the problem exists because the app opens projects by reading the selected
	 xml, the xml refers to the directory of each snps, if the directory of the snps changes, it wont be able to find it 