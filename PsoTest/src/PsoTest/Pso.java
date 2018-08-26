package PsoTest;

/**
 * Created by lfs on 2017/5/30.
 */


public class Pso {

    int n=100; //���Ӹ���������ȡ��ʮ����ȡ̫�ٻ��������
    Posiotion[] p;
    Posiotion[] v;
    double c1=3;
    double c2=1;
    Posiotion pbest[];
    Posiotion gbest;
    double w=0.3;
    double vmax=0.05;
    public void fitnessFunction(){//��Ӧ����
        for(int i=0;i<n;i++){
            double x=p[i].getX();
            double y=p[i].getY();
            if (x<30&&y<30){
                p[i].setF(30*x-y);
            }else if (x<30&&y>=30){
                p[i].setF(30*y-x);
            }else if (x>=30&&y<30){
                p[i].setF(x*x-y/2);
            }else if (x>=30&&y>=30){
                p[i].setF(20*y*y-500*x);
            }
        }
    }
    public void init(){ //��ʼ��
        p=new Posiotion[n];
        v=new Posiotion[n];
        pbest=new Posiotion[n];
        gbest=new Posiotion(0,0);
        /***
         * ��ʼ��
         */
        for(int i=0;i<n;i++){
            p[i]=new Posiotion((int)Math.random()*60,(int)Math.random()*60);
            v[i]=new Posiotion((int)Math.random()*vmax,(int)Math.random()*vmax);
        }
        fitnessFunction();
        //��ʼ����ǰ���弫ֵ�����ҵ�Ⱥ�弫ֵ
        gbest.setF(Integer.MIN_VALUE);
        for(int i=0;i<n;i++){
            pbest[i]=p[i];
            if(p[i].getF()>gbest.getF()){
                gbest=p[i];
                gbest.setF(p[i].getF());
            }
        }
        System.out.println("start gbest:"+gbest);
    }
    //����Ⱥ�㷨
    public void PSO_Method(int max){
        for(int i=0;i<max;i++){
            for(int j=0;j<n;j++){
                //����λ�ú��ٶ�
                double vx=w*v[j].getX()+c1*Math.random()*(pbest[j].getX()-p[j].getX())+c2*Math.random()*(gbest.getX()-p[j].getX());
                double vy=w*v[j].getY()+c1*Math.random()*(pbest[j].getY()-p[j].getY())+c2*Math.random()*(gbest.getY()-p[j].getY());
                if (vx>vmax) vx=vmax;
                if (vy>vmax) vy=vmax;
//                System.out.println("======"+(i+1)+"======vx:"+vx);
                v[j]=new Posiotion(vx,vy);
//                System.out.println("======"+(i+1)+"======v[j]:"+v[j]);
                p[j].setX(p[j].getX()+v[j].getX());
                p[j].setY(p[j].getY()+v[j].getY());
                //Խ���ж�
                if(p[j].getX()>=60) p[j].setX(59.9);
                if(p[j].getX()<=0) p[j].setX(0.1);
                if(p[j].getY()>=60) p[j].setY(59.9);
                if(p[j].getY()<=0) p[j].setY(0.1);
            }
            fitnessFunction();
            //���¸��弫ֵ��Ⱥ�弫ֵ
            for (int j=0;j<n;j++){
                if (pbest[j].getF()<p[j].getF()){
                    pbest[j]=p[j];
                }
                if(p[j].getF()>gbest.getF()){
                    gbest=p[j];
                    gbest.setF(p[j].getF());
                }
            }
            System.out.println("======"+(i+1)+"======gbest:"+gbest.toString());
        }


    }

    class Posiotion{
        private int x;
        private int y;
        private double f;
        Posiotion(int x,int y){
            this.x=x;
            this.y=y;
        }
       

        public double getF() {
            return f;
        }

        public void setF(double f) {
            this.f = f;
        }

        

        public int getX() {
			return x;
		}


		public void setX(int x) {
			this.x = x;
		}


		public int getY() {
			return y;
		}


		public void setY(int y) {
			this.y = y;
		}


		public String toString(){
            return " x: "+x+" y: "+y+" f: "+f;
        }
    }

    public static void main(String[] args){
        Pso ts=new Pso();
        ts.init();
        ts.PSO_Method(10000);
    }


}