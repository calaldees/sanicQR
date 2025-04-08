QR
===

```
make run
http://localhost:8000/?data=hello
```

## Consider `bash` `data:image/png;base64,`

```bash
brew install qrencode

DATA="http://test.com" echo "data:image/png;base64,$(qrencode '$DATA' -o - | base64)"
```