classdef pentoDraw < handle
    %UNTITLED Summary of this class goes here
    %   This class is the interface between matlab code and serial
    %   connection with the microprocessor
    
    properties
        figureHandle
        serial_
        pos1
        pos2
        tablePos
        a
        L1
        L2
        Axe
        Fig
        tableUp
        tableDown
    end
    
    methods
        function sP = pentoDraw(serialPort,a,L1,L2)
            if nargin > 0
                sP.serial_ = serial(serialPort, 'Baudrate', 9600);
                sP.serial_.BytesAvailableFcnMode = 'byte';
                sP.serial_.BytesAvailableFcnCount = 4;
                sP.serial_.BytesAvailableFcn = @(src,event)sP.dataReceived;
                
                
                fopen(sP.serial_);
                
            end
            if nargin > 3
                sP.a = a;
                sP.L1 = L1;
                sP.L2 = L2;
            else
                sP.a = 50;
                sP.L1 = 90;
                sP.L2 = 125;
            end
            sP.tableUp = 110;
            sP.tableDown = 80;
            sP.Axe = axes();
            sP.Fig = gcf;
            set(gcf,'CloseRequestFcn',@sP.closeWin)
            xlim([-75,75]);
            ylim([75 175]);
            set(sP.Axe,'buttondownfcn',@sP.start_pencil)
            
        end
        
        
        function delete(sP)
            fclose(sP.serial_);
            delete(sP.Fig);
        end
        
        function closeWin(sP,src,evnt)
            delete(sP);
        end
        % between 0 and 180 �
        function setPos(sP,alpha1,alpha2, tablePos)
            fwrite(sP.serial_,uint8(['P' alpha1 alpha2 tablePos]));
            disp('dataSent');
        end
        %Response from pento
        function dataReceived(obj,srcHandle,eventData)
            disp('dataReiceved');
            values = fread(obj.serial_,4);
            obj.pos1 = values(2);
            obj.pos2 = values(3);
            obj.tablePos = values(4);
        end
        
        
        
        function start_pencil(sP,src,eventdata)
            coords=get(sP.Axe,'currentpoint'); %since this is the axes callback, src=gca
            x=coords(1,1,1);
            y=coords(1,2,1);
            [a1,a2] = MGI(x,y,sP.L1,sP.L2,sP.a);
            a1 = a1 / pi * 180;
            a2 = a2 / pi * 180;
            setPos(sP,a1,a2,sP.tableDown);
            r=line(x, y, 'color', [0 .5 1], 'LineWidth', 2, 'hittest', 'off'); %turning     hittset off allows you to draw new lines that start on top of an existing line.
            set(sP.Fig,'windowbuttonmotionfcn',{@sP.continue_pencil,r})
            set(sP.Fig,'windowbuttonupfcn',@sP.done_pencil)
        end
        function continue_pencil(sP,src,eventdata,r)
            %Note: src is now the figure handle, not the axes, so we need to use gca.
            coords=get(sP.Axe,'currentpoint'); %this updates every time i move the mouse
            x=coords(1,1,1);
            y=coords(1,2,1);
            [a1,a2] = MGI(x,y,sP.L1,sP.L2,sP.a);
            a1 = a1 / pi * 180;
            a2 = a2 / pi * 180;
            setPos(sP,a1,a2,sP.tableUp);
            %get the line's existing coordinates and append the new ones.
            lastx=get(r,'xdata');
            lasty=get(r,'ydata');
            newx=[lastx x];
            newy=[lasty y];
            set(r,'xdata',newx,'ydata',newy);
        end
        function done_pencil(sP,src,evendata)
            %all this funciton does is turn the motion function off
            set(sP.Fig,'windowbuttonmotionfcn','')
            set(sP.Fig,'windowbuttonupfcn','')
            setPos(sP,sP.pos1,sP.pos2,sP.tableDown);
        end
        function drawCircle(sP,evnt,radius)
            N = 360;
            pause on;
            setPos(sP,sP.pos1,sP.pos2,sP.tableDown);
            for i=0:N
                x = radius*cos(i*2*pi/N)
                y = radius*sin(i*2*pi/N) + 125;
                [a1,a2] = MGI(x,y,sP.L1,sP.L2,sP.a);
                a1 = a1 / pi * 180
                a2 = a2 / pi * 180
                setPos(sP,a1,a2,sP.tableUp);
                %pause(2/360);
            end
            setPos(sP,sP.pos1,sP.pos2,sP.tableDown);
            
        end
        function drawLine(sP,evnt,height)
            pause on;
            setPos(sP,sP.pos1,sP.pos2,sP.tableDown);
            for i=-50:50
                x = i
                y = height;
                [a1,a2] = MGI(x,y,sP.L1,sP.L2,sP.a);
                a1 = a1 / pi * 180
                a2 = a2 / pi * 180
                setPos(sP,a1,a2,sP.tableUp);
                pause(2/360);
            end
            setPos(sP,sP.pos1,sP.pos2,sP.tableDown);
            
        end
        
    end
end

