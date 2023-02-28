import java.io.*;
import java.util.*;
 
class node4l
{
	int data;node4l link;
	node4l(int d)
	{
		data=d;link=null;
	}
}
class linkl
{
	node4l front=null,end=null;
 
	void insert(int d)
	{
		node4l temp=new node4l(d);
		if(front==null)
			{front=temp;end=temp;}
		else
		{
		   	temp.link=front;
		   	front=temp;
		}
	}
}
class linkll
{
	node4l front=null,end=null;int size=0;
 
	void insert(int d)
	{
		if(size<4)
		{
		node4l temp=new node4l(d);
		if(front==null)
			{front=temp;end=temp;size++;}
		else
		{
		   	temp.link=front;
		   	front=temp;size++;
		}
		}
	}
}
class graph
{
	linkl[] arr;int size;
	graph(int n)
	{
		size=n;
		arr=new linkl[n];
		for(int i=0;i<n;i++)
		{
			arr[i]=new linkl();
		}
	}
	void insert(int x,int y)
	{
		arr[x].insert(y);
		arr[y].insert(x);
	}
}
class dsu
{
	int [] par,size;
	dsu(int n)
	{
		par=new int[n];size=new int[n];
		for(int i=0;i<n;i++)
		{
			size[i]=1;par[i]=i;
		}
	}
	void merge(int parx,int pary)
	{
		if(size[parx]>size[pary])
		{
			par[pary]=parx;size[parx]+=size[pary];
		}
		else
		{
			par[parx]=pary;size[pary]+=size[parx];
		}
	}
	int find(int x)
	{
		if(par[x]==x)
			return x;
		else
			return find(par[x]);
	}
}
 
class NN{
 
	static linkll[][] edge;
	static int[] vis;
	static int[][] ans;
	static int[] parent;
	static linkl l;
	static int n,m,flag=0;
	static int[] temp;
	static int[][] dp;
	static graph g;
 
	static int DFS(int source,int desti,int visc)
	{
		vis[source]=visc;
		node4l temp=g.arr[source].front;
		while(temp!=null)
		{
			if(vis[temp.data]!=visc)
			{
				vis[temp.data]=visc;
				parent[temp.data]=source;
				DFS2(temp.data,desti,visc,source);
			}
			temp=temp.link;
		}
		int temp0=desti,c=0;
			while(flag==1&&temp0!=source)
			{
				c++;
				l.insert(temp0);
				temp0=parent[temp0];
			}
			l.insert(source);
			c++;
			return c;
	}
	static void DFS2(int u,int desti,int visc,int source)
	{
		
		vis[u]=visc;
		if(u==desti)
		{
			flag=1;return;
		}
		node4l temp=g.arr[u].front;
		while(temp!=null)
		{
			if(vis[temp.data]!=visc)
			{
				parent[temp.data]=u;
				DFS2(temp.data,desti,visc,source);
			}
			temp=temp.link;
		}
		
	}
 
	static int find_max(int x,int y,int visc)
	{
		if(edge[x][y].front!=null)
			return 0;
		l=new linkl();
		
		int len=DFS(x,y,visc);
		if(flag==0)
			return 0;
		flag=0;
		if(l.front==null)
			return 0;
		node4l tempr=l.front;int i=0;
		dp=new int[len][m+1];
		temp=new int[len];
		while(tempr!=null)
		{
			temp[i]=tempr.data;i++;
			tempr=tempr.link;
		}
		int max=0;
		tempr=edge[temp[0]][temp[1]].front;
		while(tempr!=null)
		{
			int tt=max(1,tempr.data);
			if(tt>max)
				max=tt;
			tempr=tempr.link;
		}
		return max;
 
 
	}
	static int max(int indx,int prev)
	{
		if(indx==dp.length-1)
			return 0;
		if(dp[indx][prev]!=0)
			return dp[indx][prev];
		else
		{
			
			node4l tempr=edge[temp[indx]][temp[indx+1]].front;
			int mx=0,ll=0;
			while(tempr!=null)
			{
				int tt=0;
				if(tempr.data==prev)
				{
					tt=max(indx+1,prev);
				}
				else
				{
					tt=1+max(indx+1,tempr.data);
				}
				if(tt>=mx)
					{mx=tt;ll=tempr.data;}
				tempr=tempr.link;
			}
			return dp[indx][prev]=mx;
		}
	}
 
 
 
	public static void main(String[] args)throws IOException
	{
		BufferedReader br=new BufferedReader(new InputStreamReader(System.in));
		String[] s=br.readLine().split(" ");
		n=Integer.parseInt(s[0]);m=Integer.parseInt(s[1]);
		g=new graph(n+1);
		dsu dsu=new dsu(n+1);
		ans=new int[n+1][n+1]; 
		parent=new int[n+1];
		vis=new int[n+1];
		edge=new linkll[n+1][n+1];
		for(int i=1;i<=n;i++)
			{for(int j=1;j<=n;j++)
				edge[i][j]=new linkll();}
 
		for(int i=0;i<m;i++)
		{
			s=br.readLine().split(" ");
			int x=Integer.parseInt(s[0]),y=Integer.parseInt(s[1]),k=Integer.parseInt(s[2]);
			edge[x][y].insert(k);
			edge[y][x].insert(k);
			int py=dsu.find(y),px=dsu.find(x);
			if(px!=py)
			{
				g.insert(x,y);
				dsu.merge(px,py);
			}
		}
 
		int q=Integer.parseInt(br.readLine());
		for(int i=0;i<q;i++)
		{
			s=br.readLine().split(" ");
			int x=Integer.parseInt(s[0]),y=Integer.parseInt(s[1]);
			if(x==y)
				System.out.println(0);
			else
			{
 
				if(ans[x][y]==0)
					{ans[x][y]=find_max(x,y,i+1);ans[y][x]=ans[x][y];}
				System.out.println(ans[x][y]);
			}
		}
		
		
	}
}