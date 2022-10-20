#!/bin/sh
curl "http://www.sleuthkit.org/sleuthkit/download.php" 2>/dev/null |grep "Download Version" |sed -e 's,.*Version ,,;s, .*,,'

