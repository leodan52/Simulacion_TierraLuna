clear

entrada=load('../datos.dat');

x1=entrada(:,1);
y1=entrada(:,2);
x2=entrada(:,3);
y2=entrada(:,4);
t=entrada(:,5);

m1=7.349e22;
m2=5.9736e24;
perigeo = 356410.0 + 1737.1 + 6371.0;

n=2;
m=1;

UML = m2/10^n;
m1 = m1/UML;
m2 = 10^n;

M=m1+m2;

x = (m1*x1+m2*x2)/M;
y = (m1*y1+m2*y2)/M;

n=length(x1);
loop1=1/60;
l=12;
a=12;

r=sqrt((x1-x2).^2 + (y1-y2).^2);
%minimo = find(r==min(r));
%maximo = find(r==max(r));
%plot(t,r)

rmax = [int2str(perigeo) ' km'];
rmin = [int2str(perigeo/2) ' km'];
tstr = int2str(t);

h = figure;
filename = 'Sistema_Tierra_Luna.gif';

for i=1:2:n
	hold off
	plot(x(i),y(i),'+r')
	hold on
	legend('Centro de masa')
	plot(x1,y1,'c')

	plot(x1(i),y1(i),'ok','LineWidth',1,'MarkerSize',10)
	plot(x2(i),y2(i),'ob','LineWidth',2,'MarkerSize',40)

	axis([ -l l -a a])
	axis equal
	grid on
	grid minor
	set(gca,'YTick',[-10 -5 0 5 10])
	set(gca,'YTicklabels',{['-' rmax],['-' rmin],'0', rmin,rmax})
	set(gca,'XTick',[-10 0 10])
	set(gca,'XTicklabels',{['-' rmax],'0',rmax})
	title('Simulación sistema Tierra-Luna')
    tiempo = ['t = ' tstr(i,:) ' días'];
    text(-l*1.2,a*0.8,tiempo)
	drawnow
        frame = getframe(h);
        im = frame2im(frame);
        [imind,cm] = rgb2ind(im,256);
        if i == 1
             imwrite(imind,cm,filename,'gif', 'Loopcount',inf,'DelayTime',loop1);
        else
            imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime',loop1);
        end
end
