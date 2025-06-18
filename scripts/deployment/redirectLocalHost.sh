#/bin/bash
killall -9 webRedirectorHttp
rm -r icicle.redirect.devel
mkdir icicle.redirect.devel
mkdir icicle.redirect.devel/cgi-bin
head -n 20 $2 >> icicle.redirect.devel/cgi-bin/googleoauthresult.py
echo "ms_ad=\""`./bin/getMsAddr.sh $1`"\"" >>  icicle.redirect.devel/cgi-bin/googleoauthresult.py
tail -n+21 $2 >> icicle.redirect.devel/cgi-bin/googleoauthresult.py
chmod -R 755 icicle.redirect.devel/
cd icicle.redirect.devel
REDIR0="<html><head><meta http-equiv=\"refresh\" content=\"2;"
REDIR1="url='http://"
REDIR2=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get services | grep $1 | awk '{print $3}'`
REDIRF=$REDIR0$REDIR1$REDIR2":"$1"/index.html'\" />"
echo $REDIRF > index.html
echo "</head><body><p>You will be redirected soon!</p></body></html>" >> index.html
webRedirectorHttp -m http.server --bind localhost --cgi $1 
