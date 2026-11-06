"""Local-only editorial UI. No dependencies required."""
import argparse,json,tempfile,threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from scout import run
ROOT=Path(__file__).parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);p.add_argument('--results',type=Path);a=p.parse_args()
 state={'report':json.loads(a.results.read_text()) if a.results else None};lock=threading.Lock()
 class Handler(BaseHTTPRequestHandler):
  def send(self,status,data,kind='application/json'):
   if not isinstance(data,bytes):data=json.dumps(data).encode()
   self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(data)
  def do_GET(self):
   if self.path=='/':self.send(200,(ROOT/'index.html').read_bytes(),'text/html; charset=utf-8')
   elif self.path=='/api/report':self.send(200,state['report'])
   else:self.send(404,{'error':'Not found'})
  def do_POST(self):
   if self.path!='/api/analyze':return self.send(404,{'error':'Not found'})
   if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{a.port}',f'http://localhost:{a.port}'):return self.send(403,{'error':'Local origin required'})
   try:
    size=int(self.headers.get('Content-Length','0'))
    if not 0<size<=10_000_000:return self.send(413,{'error':'Upload a ZIP under 10 MB'})
    if not lock.acquire(blocking=False):return self.send(409,{'error':'Run already in progress'})
    try:
     data=self.rfile.read(size)
     with tempfile.TemporaryDirectory(prefix='promo-scout-') as d:
      path=Path(d)/'input.zip';path.write_bytes(data);state['report']=run(path,Path(d)/'output');self.send(200,state['report'])
    finally:lock.release()
   except Exception as e:self.send(400,{'error':str(e)})
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);print(f'Open http://127.0.0.1:{a.port}',flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:server.server_close()
if __name__=='__main__':main()
