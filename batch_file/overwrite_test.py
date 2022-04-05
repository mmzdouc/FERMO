import sys
import os


def overwrite_test(output_file):
    '''Test to prevent overwriting files.
    
    Takes a filename output_file as input and checks if it is present in 
    current work directory. If so, the program enters an infinitive loop
    to request either a new filename (which is again checked for presence
    in current work directory), or an abort. If a new, nonexistent
    filename is presented, the program returns a filename.
     
    If file does not exist, the program simply opens and returns a 
    filename.
    '''
    if os.path.isfile(output_file):
        print("A file named ", output_file,
        " is already present in the folder.")
        print("Overwriting may lead to a malformed and non-functional .xml file.") 
        while True:
            answer = input("Overwrite? [y|n] (to abort, press ctrl+c) ").lower()
            if answer in ["y", "ye", "yes"]:
                return output_file
            if answer in ["n", "no"]:
                answer = input("Change the filename? [y|n] ").lower()
                if answer in ["y", "ye", "yes"]:
                    output_file = input("Type in the new filename: ").lower()
                    if os.path.isfile(output_file): 
                        print("A file named ", output_file, 
                        " is already present in the folder.")
                        continue
                    else:
                        return output_file
                if answer in ["n", "no"]:
                    print("A file named ", output_file, 
                    " is already present in the folder.")
                    continue 
                else:
                    print("A file named ", output_file, 
                        " is already present in the folder.")
                    continue
            else:
                print("Please type either 'y' or 'n'!")
    else:
        return output_file

 
#testing purposes
if __name__ == "__main__":
    outfile = "test.xml"
    output_file = overwrite_test(outfile)
    file_out = open(output_file, 'w')
    print("This is a test", file=file_out)

    
