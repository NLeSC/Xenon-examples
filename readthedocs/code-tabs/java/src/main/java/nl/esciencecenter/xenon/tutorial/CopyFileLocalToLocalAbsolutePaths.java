package nl.esciencecenter.xenon.tutorial;

import nl.esciencecenter.xenon.filesystems.CopyMode;
import nl.esciencecenter.xenon.filesystems.CopyStatus;
import nl.esciencecenter.xenon.filesystems.FileSystem;
import nl.esciencecenter.xenon.filesystems.Path;

public class CopyFileLocalToLocalAbsolutePaths {

    public static void main(String[] args) throws Exception {

        // use the local file system adaptor to create a file system representation
        String adaptor = "file";
        FileSystem filesystem = FileSystem.create(adaptor);

        // create Paths for the source and destination files, using absolute paths
        Path sourceFile = new Path("/home/travis/thefile.txt");
        Path destFile = new Path("/home/travis/thefile.bak");

        // create the destination file only if the destination path doesn't exist yet
        CopyMode mode = CopyMode.CREATE;
        boolean recursive = false;

        // perform the copy and wait 1000 ms for the successful or otherwise
        // completion of the operation
        String copyId = filesystem.copy(sourceFile, filesystem, destFile, mode, recursive);
        long timeoutMilliSecs = 1000;
        CopyStatus copyStatus = filesystem.waitUntilDone(copyId, timeoutMilliSecs);

        // print any exceptions
        if (copyStatus.getException() != null) {
            System.out.println(copyStatus.getException().getMessage());
        } else {
            System.out.println("File copied.");
        }
    }
}