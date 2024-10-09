using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;

  class Program {
    static void runBatchScript() {

        string scriptDir;

        if (AppDomain.CurrentDomain.FriendlyName.EndsWith(".exe"))
        {
            scriptDir = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            Console.WriteLine("Its runned by an exe");
        }
        else
        {
            // Get the directory of the script
            scriptDir = Path.GetDirectoryName(System.IO.Path.GetFullPath("passguard.bat"));
            Console.WriteLine("Is runned by script");
        }

        string batchFile = Path.Combine(scriptDir, "passguard.bat");

        string hasRunned = Path.Combine(scriptDir, "hasrunned.txt");

        if (!File.Exists(hasRunned)) {
            Process.Start(new ProcessStartInfo(batchFile) { UseShellExecute = true }).WaitForExit();

            using (File.Create(hasRunned)) {}
        }

        else {
            Console.WriteLine("Batch script has been run once");
        }
        RunCmdCommand("python3 passguard.pyw");
    }

    static void RunCmdCommand(string command)
    {
        ProcessStartInfo processInfo = new ProcessStartInfo("cmd.exe", "/c " + command);
        processInfo.RedirectStandardOutput = true;
        processInfo.RedirectStandardError = true;
        processInfo.UseShellExecute = false;
        processInfo.CreateNoWindow = true;

        Process process = new Process();
        process.StartInfo = processInfo;
        process.Start();

        // Capture and display the output of the command
        string output = process.StandardOutput.ReadToEnd();
        string error = process.StandardError.ReadToEnd();
        process.WaitForExit();

        Console.WriteLine("Output: ");
        Console.WriteLine(output);

        if (!string.IsNullOrEmpty(error))
        {
            Console.WriteLine("Error: ");
            Console.WriteLine(error);
        }
    }

    static void Main(string[] args)
    {
        runBatchScript();
    }
}

