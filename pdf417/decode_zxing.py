import subprocess
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python decode_zxing.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

# Check if file exists
if not os.path.exists(image_path):
    print(f"Error: {image_path} not found!")
    sys.exit(1)

# Check if JAR files exist
javase_jar = "javase-3.5.0.jar"
core_jar = "core-3.5.0.jar"
jcommander_jar = "jcommander-1.82.jar"

for jar in [javase_jar, core_jar, jcommander_jar]:
    if not os.path.exists(jar):
        print(f"Error: {jar} not found!")
        sys.exit(1)

print("=" * 60)
print("Decoding using ZXing library (Java)")
print("=" * 60)

# Try direct command without Docker first
try:
    command = [
        "java", "-cp",
        f"{javase_jar};{core_jar};{jcommander_jar}",
        "com.google.zxing.client.j2se.CommandLineRunner",
        image_path
    ]
    
    print(f"Running: {' '.join(command)}\n")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Decoded successfully!")
        print("\nOutput:")
        print(result.stdout)
    else:
        print("Decoding failed or no barcode found")
        print("\nStderr:")
        print(result.stderr)
        
        # Try with Docker if local Java fails
        print("\n" + "=" * 60)
        print("Trying with Docker...")
        print("=" * 60)
        
        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/app",
            "openjdk:17",
            "java", "-cp",
            f"/app/{javase_jar}:/app/{core_jar}:/app/{jcommander_jar}",
            "com.google.zxing.client.j2se.CommandLineRunner",
            f"/app/{image_path}"
        ]
        
        docker_result = subprocess.run(docker_command, capture_output=True, text=True)
        
        if docker_result.returncode == 0:
            print("Decoded successfully with Docker!")
            print("\nOutput:")
            print(docker_result.stdout)
        else:
            print("Docker decoding also failed")
            print(docker_result.stderr)
            
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("\nMake sure Java is installed or Docker is available")
