class Solution {
public:
    int prefixConnected(vector<string>& words, int k) {
        sort(words.begin(),words.end());
        int c=0;
        for(int i=0;i<words.size();i++){
            if(words[i].size()>=k){
                string m=words[i].substr(0,k);
                int j=i+1;
                int curr=0;
                while(j<words.size()){
                    if(words[j].substr(0,k)!=m){
                        break;
                    }
                    else{
                        curr++;
                    }
                    j++;
                   
                }
                if(curr>0) c++;
                 i=j-1;  
            }
                      
        }
        return c;
    }
};