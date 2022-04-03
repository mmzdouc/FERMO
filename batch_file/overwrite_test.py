import sys
import os



def overwrite_test(output_file):
    '''Test to prevent overwriting files.
    
    Takes a file output_file as input and checks if it is present in 
    current work directory. If so, the program enters an infinitive loop
    to request either a new filename (which is again checked for presence
    in current work directory), or an abort. If a new, nonexistent
    filename is presented, the program opens and returns a filehandle.
    
    If file does not exist, the program simply opens and returns a 
    filehandle to write into.
    '''
    if os.path.isfile(output_file):
        print("A file named ", output_file,
        " is already present in the folder.")
        print("Appending will lead to a malformed and non-functional .xml file.")
        while True:
            answer = input("Append? [y|n] (to abort, press ctrl+c) ").lower()
            if answer in ["y", "ye", "yes"]:
                file_out = open(output_file, 'a')
                return file_out
            if answer in ["n", "no"]:
                answer = input("Change the filename? [y|n] ").lower()
                if answer in ["y", "ye", "yes"]:
                    output_file = input("Type in the new filename: ").lower()
                    if os.path.isfile(output_file):
                        print("A file named ", output_file, 
                        " is already present in the folder.")
                        continue
                    else:
                        file_out = open(output_file, 'a')
                        return file_out
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
        file_out = open(output_file, 'a')
        return file_out


#testing purposes
if __name__ == "__main__":
    outfile = overwrite_test(sys.argv[1])
    print("This is a test", file=outfile)
