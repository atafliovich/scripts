#!/usr/local/bin/perl --
#
## AddStudents.pl
#
# Takes one argument: name of the input file.
# The input file should contain <user_name> <initial_password> per line.
##

my $position = 6; # group 6 is "CSC C69 Student"
my $addgroup = 3; # group 3 is "Student"

my $yabb_dir = "/Faculty3/atafliovich/public_html/cgi-bin/yabb2";
my $sourcedir = "/Faculty3/atafliovich/public_html/cgi-bin/yabb2/Sources";
chdir $yabb_dir;

require "$yabb_dir/Paths.pl";
require "$sourcedir/Subs.pl";
require "$sourcedir/DateTime.pl";
require "$sourcedir/Load.pl";
require "$sourcedir/System.pl";

if ( scalar(@ARGV) != 1) {
  die "Usage: AddStudents.pl <student_file>\n";
}

open (STUDENTS, "$ARGV[0]") || die "Cannot open student file: $! \n";

my @fields;
while (<STUDENTS>){
	chop;
	@fields = split(',');
	my $username = $fields[0];
        my $initial_passwd = $fields[1];
	my $real_name = $fields[3] . ' ' . $fields[2];

	if ( length($username) > 0 ) {
		adduser($username, $initial_passwd, $real_name);
	}
}

close(STUDENTS);

sub adduser{

	my $testname = shift;
	my $password = shift;
	my $real_name = shift;

        my $is_existing = &MemberIndex("check_exist", $testname);
        if ($is_existing eq $testname) {
		#### DEBUG
		print "User $testname already exists!\n";
		return;
	}

	my %member;
	$member{'passwrd1'} = $password;
	$member{'email'} = "$testname\@utsc.toronto.edu";	
	$member{'_session_id_'} = "";	
	$member{'passwrd2'} = $password;
	$member{'regdate'} = "";	
	$member{'username'} = $testname;

	$encryptopass = &encode_password($member{'passwrd1'});
	$reguser      = $member{'username'};
	$registerdate = timetostring($date);

	${$uid.$reguser}{'password'}      = $encryptopass;
	${$uid.$reguser}{'realname'}      = $real_name;
	${$uid.$reguser}{'email'}         = lc($member{'email'});
	${$uid.$reguser}{'position'}      = $position;
	${$uid.$reguser}{'addgroups'}     = $addgroup;
	${$uid.$reguser}{'postcount'}     = 0;
	${$uid.$reguser}{'usertext'}      = $defaultusertxt;
	${$uid.$reguser}{'userpic'}       = "blank.gif";
	${$uid.$reguser}{'regdate'}       = $registerdate;
	${$uid.$reguser}{'regtime'}       = int(time);
	${$uid.$reguser}{'timeselect'}    = $timeselected;
	${$uid.$reguser}{'timeoffset'}    = $timeoffset;
	${$uid.$reguser}{'dsttimeoffset'} = $dstoffset;
	${$uid.$reguser}{'hidemail'}      = 'checked';
	${$uid.$reguser}{'timeformat'}    = qq~MM D+ YYYY @ HH:mm:ss*~;
	${$uid.$reguser}{'template'}      = $new_template;
	${$uid.$reguser}{'language'}      = $language;
	${$uid.$reguser}{'pageindex'}     = qq~1|1|1~;

	&UserAccount($reguser, "register") & MemberIndex("add", $reguser) & FormatUserName($reguser);

	#### DEBUG
	print "User $testname is added successfully!\n";
}
