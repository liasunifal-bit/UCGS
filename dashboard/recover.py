
import subprocess
import os

def recover():
    try:
        out = subprocess.check_output(['git', 'show', '325ca2357ed16f36d20020c192b40543ebb79321:dashboard/index.html'], 
                                      encoding='utf-8', errors='ignore')
        print("Git show success. Total length:", len(out))
        
        with open('index_recovered.html', 'w', encoding='utf-8') as f:
            f.write(out)
        print("Written to index_recovered.html")
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    recover()
