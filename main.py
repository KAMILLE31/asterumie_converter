import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

def decompose_hangul(syllable):
    BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    char_code = ord(syllable) - BASE_CODE
    chosung_index = char_code // CHOSUNG
    jungsung_index = (char_code - (CHOSUNG * chosung_index)) // JUNGSUNG
    jongsung_index = (char_code - (CHOSUNG * chosung_index) - (JUNGSUNG * jungsung_index))

    return CHOSUNG_LIST[chosung_index], JUNGSUNG_LIST[jungsung_index], JONGSUNG_LIST[jongsung_index]

def decompose_string(input_str):
    result = []
    for char in input_str:
        if '가' <= char <= '힣':
            chosung, jungsung, jongsung = decompose_hangul(char)
            result.append(chosung + jungsung + (jongsung if jongsung != ' ' else ''))
        else:
            if char == ' ':
                result.append('  ')  # 공백을 두 칸으로 변경
            else:
                result.append(char)  # 한글이 아닌 문자(공백 포함)를 그대로 추가
    return ''.join(result)

class RequestHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        input_str = data['input']
        decomposed_str = decompose_string(input_str)
        response = {'output': decomposed_str}
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
