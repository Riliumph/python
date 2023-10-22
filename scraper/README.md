# scraper

seleniumによりWEBページを取得し、BeautifulSoupでHTMLを解析するサンプルを作る。

> 攻撃にならないようなURLを使うこと。

## インストールが必要なもの

Google ChromeをDockerfileでインストールしようとすると、インストールが完了する前にステージが削除されようとしてエラーになる。

```console
$ sudo apt update
$ sudo apt install -y google-chrome-stable
```

以下のコマンドでGoogleの起動オプションが確認できる。

```console
$ google-chrome --no-sandbox --headless --disable-gpu --screenshot="screenshot_$(date +"%Y%m%d").png" --window-size=1280,1080 https://www.ugtop.com/spill.shtml
```

## chromedriver-binary

Google Chromeとseleniumが用いるchromedriverはバージョンを揃える必要がある。

> 異なっていると以下のエラーになる。  
> The chromedriver version (120.0.6081.0) detected in PATH at /home/vscode/.local/lib/python3.11/site-packages/chromedriver_binary/chromedriver might not be compatible with the detected chrome version (118.0.5993.88); currently, chromedriver 118.0.5993.70 is recommended for chrome 118.*, so it is advised to delete the driver in PATH and retry

今回は、Google Chrome(118.0.5993.88)が遅れており、ドライバー(120.0.6081.0)が先行している。  
requirements.txtを変更してドライバーのバージョンを下げよう。

```txt
chromedriver-binary==118.*
```
