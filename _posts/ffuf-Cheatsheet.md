# ffuf (Fuzz Faster U Fool) Cheatsheet 

## 1. Core Options

| Option | Description | Example |
|--------|-------------|---------|
| `-u` | Target URL (use FUZZ keyword) | `-u https://target/FUZZ` |
| `-w` | Wordlist path with optional keyword | `-w wordlist.txt` or `-w list.txt:KEYWORD` |
| `-t` | Number of threads (default: 40) | `-t 100` |
| `-rate` | Requests per second | `-rate 50` |
| `-p` | Delay between requests (seconds or range) | `-p 0.1` or `-p 0.1-2.0` |
| `-X` | HTTP method | `-X POST` |
| `-d` | POST data | `-d "user=admin&pass=FUZZ"` |
| `-H` | Add header (repeatable) | `-H "Authorization: Bearer token"` |
| `-b` | Cookies | `-b "session=abc123; user=admin"` |
| `-r` | Follow redirects | `-r` |
| `-x` | Proxy (HTTP/SOCKS5) | `-x http://127.0.0.1:8080` |
| `-timeout` | Request timeout (default: 10s) | `-timeout 15` |

---

## 2. Matcher Options (what to show)

| Option | Description | Example |
|--------|-------------|---------|
| `-mc` | Match HTTP status codes | `-mc 200,302,401` |
| `-ms` | Match response size (bytes) | `-ms 500,1000-1200` |
| `-mw` | Match word count | `-mw 100,200-220` |
| `-ml` | Match line count | `-ml 10,15-20` |
| `-mr` | Match regex in response | `-mr "admin\|root"` |

---

## 3. Filter Options (what to hide)

| Option | Description | Example |
|--------|-------------|---------|
| `-fc` | Filter HTTP status codes | `-fc 404,403` |
| `-fs` | Filter response size (bytes) | `-fs 0,1234` |
| `-fw` | Filter word count | `-fw 0,300-400` |
| `-fl` | Filter line count | `-fl 0,50-60` |
| `-fr` | Filter regex in response | `-fr "Not Found"` |

---

## 4. Input Options

| Option | Description | Example |
|--------|-------------|---------|
| `-w` | Wordlist file path | `-w /usr/share/wordlists/dirb/common.txt` |
| `-w list:KEYWORD` | Wordlist with custom keyword | `-w dirs.txt:DIR -u https://target/DIR` |
| `-e` | File extensions (comma-separated) | `-e .php,.html,.js` |
| `-D` | DirSearch compatibility mode | `-D -e php,html` |
| `-mode` | Multi-wordlist mode | `-mode clusterbomb` or `-mode pitchfork` |
| `-request` | Raw HTTP request file | `-request req.txt` |
| `-request-proto` | Protocol for raw request | `-request-proto https` |
| `-input-cmd` | Command producing input | `-input-cmd "seq 1 1000"` |
| `-input-num` | Number of inputs (with -input-cmd) | `-input-num 100` |
| `-ic` | Ignore wordlist comments | `-ic` |

---

## 5. Recursion Options

| Option | Description | Example |
|--------|-------------|---------|
| `-recursion` | Enable recursion (URL must end in FUZZ) | `-recursion` |
| `-recursion-depth` | Max recursion depth (default: 0) | `-recursion-depth 2` |
| `-recursion-strategy` | Strategy: `default` or `greedy` | `-recursion-strategy greedy` |

---

## 6. Output Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o` | Output file | `-o results.json` |
| `-of` | Output format | `-of json,html,csv,md,ecsv,ejson,all` |
| `-od` | Directory for matched responses | `-od ./output/` |
| `-or` | Only create output if results exist | `-or` |
| `-debug-log` | Write debug logs | `-debug-log debug.txt` |

---

## 7. General Options

| Option | Description | Example |
|--------|-------------|---------|
| `-V` | Show version | `-V` |
| `-c` | Colorize output | `-c` |
| `-v` | Verbose (show full URL and redirects) | `-v` |
| `-s` | Silent mode (minimal output) | `-s` |
| `-ac` | Auto-calibrate filters | `-ac` |
| `-acc` | Custom auto-calibration string | `-acc "404 page"` |
| `-maxtime` | Max total runtime (seconds) | `-maxtime 3600` |
| `-maxtime-job` | Max runtime per job (seconds) | `-maxtime-job 60` |
| `-sf` | Stop when >95% return 403 | `-sf` |
| `-se` | Stop on spurious errors | `-se` |
| `-sa` | Stop on all errors (implies -sf -se) | `-sa` |
| `-config` | Load config from file | `-config ffuf.conf` |
| `-replay-proxy` | Replay matched requests via proxy | `-replay-proxy http://127.0.0.1:8080` |
| `-ignore-body` | Don't fetch response body | `-ignore-body` |

---

## 8. Common Use Cases

| Task | Command |
|------|---------|
| **Directory fuzzing** | `ffuf -u https://target/FUZZ -w wordlist.txt -fc 404` |
| **File discovery with extensions** | `ffuf -u https://target/FUZZ -w wordlist.txt -e .php,.html,.js` |
| **Subdomain enumeration** | `ffuf -u https://FUZZ.target.com -w subdomains.txt -fs 1234` |
| **Virtual host discovery** | `ffuf -u http://target/ -H "Host: FUZZ.target" -w vhosts.txt` |
| **Parameter fuzzing (GET)** | `ffuf -u "https://target/page?FUZZ=value" -w params.txt` |
| **POST body fuzzing** | `ffuf -u https://target/login -X POST -d "user=admin&pass=FUZZ" -w passwords.txt -H "Content-Type: application/x-www-form-urlencoded"` |
| **JSON POST fuzzing** | `ffuf -u https://target/api -X POST -d '{"user":"admin","pass":"FUZZ"}' -H "Content-Type: application/json" -w passwords.txt` |
| **Header fuzzing** | `ffuf -u https://target/ -H "X-Custom: FUZZ" -w headers.txt` |
| **Recursive directory scan** | `ffuf -u https://target/FUZZ -w wordlist.txt -recursion -recursion-depth 2` |
| **Multi-wordlist (clusterbomb)** | `ffuf -u https://target/W1/W2 -w dirs.txt:W1 -w files.txt:W2 -mode clusterbomb` |
| **Multi-wordlist (pitchfork)** | `ffuf -u https://target/W1/W2 -w a.txt:W1 -w b.txt:W2 -mode pitchfork` |
| **Through Burp proxy** | `ffuf -u https://target/FUZZ -w wordlist.txt -x http://127.0.0.1:8080` |
| **Rate limited scan** | `ffuf -u https://target/FUZZ -w wordlist.txt -rate 10 -p 0.5` |
| **Auto-calibrate filters** | `ffuf -u https://target/FUZZ -w wordlist.txt -ac` |
| **Raw request from file** | `ffuf -request req.txt -request-proto https -w wordlist.txt` |
| **Save matched responses** | `ffuf -u https://target/FUZZ -w wordlist.txt -od ./matched/` |
| **JSON output** | `ffuf -u https://target/FUZZ -w wordlist.txt -o results.json -of json` |

---

## 9. Filter/Match Quick Reference

| Goal | Option | Example |
|------|--------|---------|
| Show only 200 OK | `-mc 200` | `-mc 200` |
| Hide 404 Not Found | `-fc 404` | `-fc 404` |
| Hide empty responses | `-fs 0` | `-fs 0` |
| Hide specific size | `-fs 1234` | `-fs 1234` |
| Match regex (admin found) | `-mr "admin"` | `-mr "admin"` |
| Filter regex (error page) | `-fr "Error\|Not Found"` | `-fr "Error"` |
| Match word count range | `-mw 50-100` | `-mw 50-100` |
| Filter line count | `-fl 0,20-30` | `-fl 0,20-30` |

---

## 10. Pro Tips Table

| Tip | Command |
|-----|---------|
| Start with broad match, refine with filters | `ffuf -u https://target/FUZZ -w big.txt -mc all` then add `-fs` |
| Baseline response size first | Run once, note common size, then `-fs <size>` |
| Use auto-calibrate for custom 404s | `-ac` or `-acc "custom 404 string"` |
| Save matched responses for later analysis | `-od ./output/` |
| Throttle aggressive scans | `-rate 20 -p 0.1-0.5` |
| Proxy through Burp for manual review | `-x http://127.0.0.1:8080` |
| Use verbose for debugging | `-v` |
| Combine filters | `-fc 404,403 -fs 0,1234 -fw 100-200` |
