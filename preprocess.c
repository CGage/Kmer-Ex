#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <dirent.h>

int preProcessChroms(char filePath[]) {
	DIR *d;
	struct dirent *dir;
	d = opendir(filePath);

	int i  = 0;
	while ((dir = readdir(d)) != NULL) {
		if (!strcmp(&dir->d_name[(strlen(dir->d_name) > 4) ? (strlen(dir->d_name) - 3) : 0], ".fa")) {
			char path[100] = "";
			strcat(path, filePath);
			strcat(path, dir->d_name);

			char removeHeader[100]; 
			sprintf(removeHeader, "grep -v \">\" %s > temp1.txt",path);
			system(removeHeader);
			char removeNewline[100];
			sprintf(removeNewline, "awk '{printf $0""}' temp1.txt > temp2.txt");
			system(removeNewline);
			char toLower[100];
			sprintf(toLower, "tr '[a-z]' '[A-Z]' < temp2.txt > %s1", path);
			system(toLower);

			char addEOL[100];
			sprintf(addEOL, "echo '\n' >> %s1", path);
			system(addEOL);

			printf("%s : Header, toUpper and Newline removed\n", dir->d_name);
		}
	}
	system("rm temp1.txt temp2.txt");
	return 0;
}

int main(int argc, char* argv[]) {
	preProcessChroms(argv[1]);
	return 0;
}
