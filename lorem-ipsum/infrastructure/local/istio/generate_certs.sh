openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -subj '/O=example Inc./CN=ipsum.dev' -keyout ipsum.dev.key -out ipsum.dev.crt
openssl req -out lorem.ipsum.dev.csr -newkey rsa:2048 -nodes -keyout lorem.ipsum.dev.key -subj "/CN=lorem.ipsum.dev/O=lorem organization"
openssl x509 -req -days 365 -CA ipsum.dev.crt -CAkey ipsum.dev.key -set_serial 0 -in lorem.ipsum.dev.csr -out lorem.ipsum.dev.crt

kubectl create -n istio-system secret tls lorem-ipsum-dev-credential --key=lorem.ipsum.dev.key --cert=lorem.ipsum.dev.crt

