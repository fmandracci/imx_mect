#!/bin/sh

decodeURL() {
echo $1 | sed ' s/%20/\ /g; s/%21/\!/g; s/%22/\"/g;
		s/%23/\#/g; s/%24/\$/g; s/%25/\%/g; 
		s/%26/\&/g; s/%27/\ /g; s/%28/\(/g;
		s/%29/\)/g; s/%2A/\*/g; s/%2B/\+/g;
		s/%2C/\,/g; s/%2D/\-/g; s/%2E/\./g;
		s/%2F/\//g; s/%3A/\:/g; s/%3B/\;/g;
		s/%3C/\</g; s/%3D/\=/g; s/%3E/\>/g;
		s/%3F/\?/g; s/%40/\@/g; s/%5B/\[/g;
		s/%5C/\\/g; s/%5D/\]/g; s/%5E/\^/g;
		s/%5F/\_/g; s/%60/\ /g; s/%7B/\{/g;
		s/%7C/\|/g; s/%7D/\}/g; s/%7E/\~/g;
		'
}

DATA=`cat`

. ./load.cgi

ERROR=0

for x in `echo $DATA | tr "&" "\n"`; do
   if [ "$x" != "delete=Delete" ] && [ "$x" != "download=Download" ] && [ ! `echo $x | grep ROOT_DIR` ]
   then
   	  FULLPATHFILE=`echo $x | cut -d= -f2 | sed s/'%2F'/'\/'/g`
	  FILE=`basename $FULLPATHFILE`
	  FILE=$(decodeURL $FILE)
   	  DIRECTORY=`dirname $FULLPATHFILE`
   	  FILESTOACTION="$FILESTOACTION $FILE "
	  if [ "$DIRECTORY" == "$BASE_DIR/$ALARMS_DIR" ]
	  then
		$SIGN $FULLPATHFILE | cut -d\  -f1 > $FULLPATHFILE.sign
		ERROR=$?
		if [ "$ERROR" != "0" ]
		then
			break;
		fi
		FILESTOACTION="$FILESTOACTION $FILE.sign"
	  fi
   else 
   	if [ `echo $x | grep ROOT_DIR` ]
	then
		ROOT_DIR=`echo $x | cut -d= -f2 | sed s/'%2F'/'\/'/g`
	fi
   fi
done

# trim the initial and final spaces
FILESTOACTION=`echo $FILESTOACTION`

if [ "`echo $DATA | grep -c delete`" == "1" ]
then
   ACTION="delete"
else
   ACTION="download"
fi

# nothing to do
if [ "$FILESTOACTION" == "" ]
then
cat <<EOF
Content-Type: text/html

<html>
<head>
<title> Files Manager </title>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div id="container">
		<div id="header">
			<table width="100%">
				<tr align="left">
					<td>
						<h1><img src="$LOGO_NAME" style="width:auto;height:136px;float=left;vertical-align:middle;">  $TARGET_NAME Files Manager</h1>
					</td>
					<td>
EOF
. $OLD_DIR/info.cgi
cat <<EOF
					</td>
				</tr>
			</table>
		</div> <!-- end div header -->
<center>
<div id="content">
<table style="border:solid 2px #335970;" bgcolor=#f1fbff cellspacing=10 cellpadding=4 align=center >
<tbody>
<tr>
<td>
    nothing to $ACTION
</td>
</tr>
</tbody>
</table>
</div>                                                                                
EOF
echo "      <input class=bottoni type=\"button\" value=\"Home\" onclick=\"window.location.href='$HOME_PAGE'\">"
echo "      <input class=bottoni type=\"button\" value=\"Back\" onclick=\"window.location.href='filebrowser.cgi?ROOT_DIR=$ROOT_DIR'\">"
cat <<EOF
</center>
</div>                                                                                
</body>
</html>
EOF
exit 0
fi

# go into the files directory
OLD_DIR=`pwd`
cd $DIRECTORY

if [ "$ERROR" == "0" ]
then
# crea zip file
if [ "$ACTION" != "delete" ]
then
   # zip log file
   if [ "`echo $FILESTOACTION | wc -w`" == "1" ]
   then
      zipfilename=$FILESTOACTION.zip
   else
      zipfilename=`date '+%Y_%m_%d'`_`date '+%H%M%S'`.zip
   fi
   /usr/bin/zip -q -r $zipfilename $FILESTOACTION
   ERROR=$?
fi
fi

# clean the sign file
for x in $FILESTOACTION; do
	if [ `echo $x | grep .sign$` ]
	then
		rm -f $x
	fi
done

if [ "$ERROR" == "0" ]
then
# download
if [ "$ACTION" == "download" ]
then
cat <<EOF
Content-type: multipart/x-zip
Content-disposition: attachment; filename="$zipfilename"

EOF
	cat $zipfilename
	rm -f $zipfilename
else
# delete
	rm -rf $FILESTOACTION
cat <<EOF
Content-Type: text/html

<html>
<head>
<title> REMOTE UPDATER </title>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div id="container">
		<div id="header">
			<table width="100%">
				<tr align="left">
					<td>
						<h1><img src="$LOGO_NAME" style="width:auto;height:136px;float=left;vertical-align:middle;">  $TARGET_NAME Files Manager</h1>
					</td>
					<td>
EOF
. $OLD_DIR/info.cgi
cat <<EOF
					</td>
				</tr>
			</table>
		</div> <!-- end div header -->
<center>
<div id="content">
<table style="border:solid 2px #335970;" bgcolor=#f1fbff cellspacing=10 cellpadding=4 align=center >
<tbody>
<tr>
<td>
    Success to $ACTION $FILESTOACTION $ROOT_DIR.
</td>
</tr>
</tbody>
</table>
</div>                                                                                
EOF
echo "      <input class=bottoni type=\"button\" value=\"Home\" onclick=\"window.location.href='$HOME_PAGE'\">"
echo "      <input class=bottoni type=\"button\" value=\"Back\" onclick=\"window.location.href='filebrowser.cgi?ROOT_DIR=$ROOT_DIR'\">"
cat <<EOF
</center>
</div>                                                                                
</body>
</html>

EOF
fi
else
cat <<EOF
Content-Type: text/html


<html>
<head>
<title> REMOTE UPDATER </title>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div id="container">
		<div id="header">
			<table width="100%">
				<tr align="left">
					<td>
						<h1><img src="$LOGO_NAME" style="width:auto;height:136px;float=left;vertical-align:middle;">  $TARGET_NAME Files Manager</h1>
					</td>
					<td>
EOF
. $OLD_DIR/info.cgi
cat <<EOF
					</td>
				</tr>
			</table>
		</div> <!-- end div header -->
<center>
<div id="content">

<table style="border:solid 2px #FF0000;" bgcolor=#fffbff cellspacing=10 cellpadding=4 align=center >
<tbody>
<tr>
<td>
    Fail to $ACTION $FILESTOACTION.
</td>
</tr>
</tbody>
</table>
</div>
EOF
echo "      <input class=bottoni type=\"button\" value=\"Home\" onclick=\"window.location.href='$HOME_PAGE'\">"
cat <<EOF
      <input class=bottoni type="button" value="Back" onclick="window.location.href='menu.cgi'">
</center>
</div>                                                                                
</body>
</html>

EOF
fi

cd $OLD_DIR
