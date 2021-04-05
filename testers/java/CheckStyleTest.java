import static org.junit.Assert.assertEquals;

import edu.toronto.cs.jam.annotations.Description;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.Test;

public class CheckStyleTest {

  @Test(timeout = 10000) // checkstyle takes long, need a larger value for timeout
  @Description(description = "Testing whether checkstyle passes.")
  public void testCheckstyle() throws IOException, InterruptedException {

    List<String> files = Arrays.asList(new String[] { "Pair.java", "Interleaver.java"});
    String cwd = System.getProperty("user.dir");
    String command = "java -jar /home/anya/projects/at/uam/jam/lib/checkstyle-8.40-all.jar "
        + "-c /home/anya/projects/at/uam/jam/styles/google_checks.xml "
        + files.stream().map(s -> cwd + "/poly/" + s).collect(Collectors.joining(" "));

    Process process = Runtime.getRuntime().exec(command);

    BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
    // BufferedReader br = new BufferedReader(new
    // InputStreamReader(p.getErrorStream()));
    String actual = br.lines().collect(Collectors.joining());
    actual = actual
        .replace("/home/anya/courses/c24/cscc24winter2021/exercises/e4/marking/java/submissions",
            "...")
        .trim();
    actual = actual.substring(0, Math.min(actual.length(), 1000));
    process.waitFor();
    String expected = "Starting audit...Audit done.";

    assertEquals(String.format("Checkstyle failed: %s.", actual), expected.trim(), actual.trim());
  }
}
