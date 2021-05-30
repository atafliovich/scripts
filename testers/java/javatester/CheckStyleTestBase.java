package javatester;

import static org.junit.Assert.assertEquals;

import edu.toronto.cs.jam.annotations.Description;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.Test;

public class CheckStyleTestBase {

  final int TIMEOUT = 10000;
  final int MAX_LENGTH = 1000;

  protected String markingDir;
  protected String packageName;
  protected String[] fileNames;

  @Test(timeout = TIMEOUT)
  @Description(description = "Testing whether checkstyle passes.")
  public void testCheckstyle() throws IOException, InterruptedException {

    List<String> files = Arrays.asList(fileNames);
    String cwd = System.getProperty("user.dir");
    String command = "java -jar /home/anya/projects/at/uam/jam/lib/checkstyle.jar "
        + "-c /home/anya/projects/at/uam/jam/styles/google_checks.xml " + files.stream()
            .map(s -> cwd + "/" + packageName + "/" + s).collect(Collectors.joining(" "));

    Process process = Runtime.getRuntime().exec(command);
    BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
    String actual = br.lines().collect(Collectors.joining()).replace(markingDir, "...").trim();
    actual = actual.substring(0, Math.min(actual.length(), MAX_LENGTH));
    process.waitFor();

    String expected = "Starting audit...Audit done.";

    assertEquals(String.format("Checkstyle failed: %s.", actual), expected.trim(), actual.trim());
  }
}
