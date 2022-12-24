#!/usr/bin/env python3

#################################################
############### Silvana Cardoso #################
######## https://github.com/silvana-cardoso #####
########### Last update: 12/24/22 ###############
#################################################

#########################################################################
##### PyQt5 interface to control 21 piezos based on asyncio package######
################### controllers: newfocus8742 ###########################
#########################################################################

import sys
import asyncio
import threading
import queue as Queue
from PyQt5 import QtWidgets, uic, QtGui
from matplotlib.pyplot import flag, step
from newfocus8742.tcp_nf import NewFocus8742TCP as tcp

icon_green_led = './icons/green-led-on.png'

icon_red_led = './icons/led-red-on.png'

icon_arrow_black = './icon/arrow-black'

# chield of the class QtWidgets.QMainWindow
class GuiPiezos(QtWidgets.QMainWindow):

    def __init__(self,loop):

        # super is used to give access to methos of the parent class
        super(GuiPiezos, self).__init__()
        uic.loadUi('piezos_gui.ui',self)

        self.pushButtonResetAll.clicked.connect(self.reset_controlers)

        self.queue_axis_infos = Queue.Queue()
        self.queue_axis_v = Queue.Queue(1)
        self.queue_axis_a = Queue.Queue(1)
        self.flag_movement = True
        self.loop = loop

        ###################################################################################
        #####################################general tab###################################
        ###################################################################################
        
        # the piezos are grouped in seven boxes with three piezos each
        # boxes are named UR, UL, OR, OC, OL, DR, DL
        # for each box, the piezos are p1, p2 and p3

        #########################
        ### setup     UR  box ###
        #########################

        # move p1,p2 and p3
        self.mov_UR = [[2,1],[3,1],[1,1]]

        # setup go push button
        self.pushButtonGoURm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoURm))
        self.pushButtonGoURp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoURp))
        
        self.pushButtonGoURP1m.clicked.connect(lambda: self.thread(self.pushButtonGoURP1m))
        self.pushButtonGoURP2m.clicked.connect(lambda: self.thread(self.pushButtonGoURP2m))
        self.pushButtonGoURP3m.clicked.connect(lambda: self.thread(self.pushButtonGoURP3m))
        self.pushButtonGoURP1p.clicked.connect(lambda: self.thread(self.pushButtonGoURP1p))
        self.pushButtonGoURP2p.clicked.connect(lambda: self.thread(self.pushButtonGoURP2p))
        self.pushButtonGoURP3p.clicked.connect(lambda: self.thread(self.pushButtonGoURP3p))
        
        # setup abort push button
        self.pushButtonAbortUR.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortUR))

        #########################
        ### setup     UL  box ###
        #########################

        # move p1,p2 and p3
        self.mov_UL = [[2,1],[1,1],[3,1]]

        # setup go push button
        self.pushButtonGoULm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoULm))
        self.pushButtonGoULp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoULp))

        self.pushButtonGoULP1m.clicked.connect(lambda: self.thread(self.pushButtonGoULP1m))
        self.pushButtonGoULP2m.clicked.connect(lambda: self.thread(self.pushButtonGoULP2m))
        self.pushButtonGoULP3m.clicked.connect(lambda: self.thread(self.pushButtonGoULP3m))
        self.pushButtonGoULP1p.clicked.connect(lambda: self.thread(self.pushButtonGoULP1p))
        self.pushButtonGoULP2p.clicked.connect(lambda: self.thread(self.pushButtonGoULP2p))
        self.pushButtonGoULP3p.clicked.connect(lambda: self.thread(self.pushButtonGoULP3p))

        # setup abort push button
        self.pushButtonAbortUL.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortUL))

        ##########################
        #### setup     or  box ###
        ##########################

        # move p1,p2 and p3
        self.mov_OR = [[2,2],[3,2],[1,2]]

        # setup go push button
        self.pushButtonGoORm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoORm))
        self.pushButtonGoORp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoORp))

        self.pushButtonGoORP1m.clicked.connect(lambda: self.thread(self.pushButtonGoORP1m))
        self.pushButtonGoORP2m.clicked.connect(lambda: self.thread(self.pushButtonGoORP2m))
        self.pushButtonGoORP3m.clicked.connect(lambda: self.thread(self.pushButtonGoORP3m))
        self.pushButtonGoORP1p.clicked.connect(lambda: self.thread(self.pushButtonGoORP1p))
        self.pushButtonGoORP2p.clicked.connect(lambda: self.thread(self.pushButtonGoORP2p))
        self.pushButtonGoORP3p.clicked.connect(lambda: self.thread(self.pushButtonGoORP3p))
        
        # setup abort push button
        self.pushButtonAbortOR.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortOR))

        #########################
        ### setup     OC  box ###
        #########################

        self.mov_OC = [[2,4],[3,4],[1,4]] # move p1,p2 and p3

        # setup go push button
        self.pushButtonGoOCm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoOCm))
        self.pushButtonGoOCp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoOCp))

        self.pushButtonGoOCP1m.clicked.connect(lambda: self.thread(self.pushButtonGoOCP1m))
        self.pushButtonGoOCP2m.clicked.connect(lambda: self.thread(self.pushButtonGoOCP2m))
        self.pushButtonGoOCP3m.clicked.connect(lambda: self.thread(self.pushButtonGoOCP3m))
        self.pushButtonGoOCP1p.clicked.connect(lambda: self.thread(self.pushButtonGoOCP1p))
        self.pushButtonGoOCP2p.clicked.connect(lambda: self.thread(self.pushButtonGoOCP2p))
        self.pushButtonGoOCP3p.clicked.connect(lambda: self.thread(self.pushButtonGoOCP3p))
        
        # setup abort push button
        self.pushButtonAbortOC.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortOC))

        ##########################
        #### setup     ol  box ###
        ##########################

        self.mov_OL = [[2,2],[3,2],[1,2]] # move p1,p2 and p3

        # setup go push button
        self.pushButtonGoOLm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoOLm))
        self.pushButtonGoOLp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoOLp))

        self.pushButtonGoOLP1m.clicked.connect(lambda: self.thread(self.pushButtonGoOLP1m))
        self.pushButtonGoOLP2m.clicked.connect(lambda: self.thread(self.pushButtonGoOLP2m))
        self.pushButtonGoOLP3m.clicked.connect(lambda: self.thread(self.pushButtonGoOLP3m))
        self.pushButtonGoOLP1p.clicked.connect(lambda: self.thread(self.pushButtonGoOLP1p))
        self.pushButtonGoOLP2p.clicked.connect(lambda: self.thread(self.pushButtonGoOLP2p))
        self.pushButtonGoOLP3p.clicked.connect(lambda: self.thread(self.pushButtonGoOLP3p))
        
        # setup abort push button
        self.pushButtonAbortOL.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortOL))

        # setup     DR  box
        self.mov_DR = [[2,3],[3,3],[1,3]] # move p1,p2 and p3
        # setup go push button
        # self.pushButtonGoDR.clicked.connect(lambda: self.exec_movement(self.pushButtonGoDR))
        self.pushButtonGoDRm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoDRm))
        self.pushButtonGoDRp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoDRp))

        self.pushButtonGoDRP1m.clicked.connect(lambda: self.thread(self.pushButtonGoDRP1m))
        self.pushButtonGoDRP2m.clicked.connect(lambda: self.thread(self.pushButtonGoDRP2m))
        self.pushButtonGoDRP3m.clicked.connect(lambda: self.thread(self.pushButtonGoDRP3m))
        self.pushButtonGoDRP1p.clicked.connect(lambda: self.thread(self.pushButtonGoDRP1p))
        self.pushButtonGoDRP2p.clicked.connect(lambda: self.thread(self.pushButtonGoDRP2p))
        self.pushButtonGoDRP3p.clicked.connect(lambda: self.thread(self.pushButtonGoDRP3p))
        
        # setup abort push button
        self.pushButtonAbortDR.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortDR))

        #########################
        ### setup     DL  box ###
        #########################

        self.mov_DL = [[3,3],[1,3],[2,3]] # move p1,p2 and p3

        # setup go push button
        # self.pushButtonGoDL.clicked.connect(lambda: self.exec_movement(self.pushButtonGoDL))
        self.pushButtonGoDLm.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoDLm))
        self.pushButtonGoDLp.clicked.connect(lambda: self.thread_go_all(self.pushButtonGoDLp))
        self.pushButtonGoDLP1m.clicked.connect(lambda: self.thread(self.pushButtonGoDLP1m))
        self.pushButtonGoDLP2m.clicked.connect(lambda: self.thread(self.pushButtonGoDLP2m))
        self.pushButtonGoDLP3m.clicked.connect(lambda: self.thread(self.pushButtonGoDLP3m))
        self.pushButtonGoDLP1p.clicked.connect(lambda: self.thread(self.pushButtonGoDLP1p))
        self.pushButtonGoDLP2p.clicked.connect(lambda: self.thread(self.pushButtonGoDLP2p))
        self.pushButtonGoDLP3p.clicked.connect(lambda: self.thread(self.pushButtonGoDLP3p))
        
        # setup abort push button
        self.pushButtonAbortDL.clicked.connect(lambda: self.abort_mov(self.pushButtonAbortDL))

        ###################################################################################
        #####################################tab Config####################################
        ###################################################################################
        
        # get velocity and acceleration values
        self.infos(ctrs1,self.mov_UR[0])
        self.infos(ctrs1,self.mov_UR[1])
        self.infos(ctrs1,self.mov_UR[2])

        self.infos(ctrs2,self.mov_UL[0])
        self.infos(ctrs2,self.mov_UL[1])
        self.infos(ctrs2,self.mov_UL[2])

        self.infos(ctrs1,self.mov_OR[0])
        self.infos(ctrs1,self.mov_OR[1])
        self.infos(ctrs1,self.mov_OR[2])

        self.infos(ctrs1,self.mov_OC[0])
        self.infos(ctrs1,self.mov_OC[1])
        self.infos(ctrs1,self.mov_OC[2])

        self.infos(ctrs2,self.mov_OL[0])
        self.infos(ctrs2,self.mov_OL[1])
        self.infos(ctrs2,self.mov_OL[2])

        self.infos(ctrs1,self.mov_DR[0])
        self.infos(ctrs1,self.mov_DR[1])
        self.infos(ctrs1,self.mov_DR[2])

        self.infos(ctrs2,self.mov_DL[0])
        self.infos(ctrs2,self.mov_DL[1])
        self.infos(ctrs2,self.mov_DL[2])

        # change velocity

        self.spinBoxSetV.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV,ctrs1,self.mov_UR[0]))
        self.spinBoxSetV_2.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_2,ctrs1,self.mov_UR[1]))
        self.spinBoxSetV_3.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_3,ctrs1,self.mov_UR[2]))

        self.spinBoxSetV_4.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_4,ctrs2,self.mov_UL[0]))
        self.spinBoxSetV_5.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_5,ctrs2,self.mov_UL[1]))
        self.spinBoxSetV_6.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_6,ctrs2,self.mov_UL[2]))

        self.spinBoxSetV_7.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_7,ctrs1,self.mov_OR[0]))
        self.spinBoxSetV_8.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_8,ctrs1,self.mov_OR[1]))
        self.spinBoxSetV_9.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_9,ctrs1,self.mov_OR[2]))

        self.spinBoxSetV_10.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_10,ctrs1,self.mov_OC[0]))
        self.spinBoxSetV_11.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_11,ctrs1,self.mov_OC[1]))
        self.spinBoxSetV_12.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_12,ctrs1,self.mov_OC[2]))

        self.spinBoxSetV_13.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_13,ctrs2,self.mov_OL[0]))
        self.spinBoxSetV_14.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_14,ctrs2,self.mov_OL[1]))
        self.spinBoxSetV_15.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_15,ctrs2,self.mov_OL[2]))

        self.spinBoxSetV_16.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_16,ctrs1,self.mov_DR[0]))
        self.spinBoxSetV_17.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_17,ctrs1,self.mov_DR[1]))
        self.spinBoxSetV_18.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_18,ctrs1,self.mov_DR[2]))

        self.spinBoxSetV_19.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_19,ctrs2,self.mov_DL[0]))
        self.spinBoxSetV_20.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_20,ctrs2,self.mov_DL[1]))
        self.spinBoxSetV_21.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetV_21,ctrs2,self.mov_DL[2]))


        # change acceleration

        self.spinBoxSetA.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA,ctrs1,self.mov_UR[0]))
        self.spinBoxSetA_2.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_2,ctrs1,self.mov_UR[1]))
        self.spinBoxSetA_3.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_3,ctrs1,self.mov_UR[2]))

        self.spinBoxSetA_4.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_4,ctrs2,self.mov_UL[0]))
        self.spinBoxSetA_5.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_5,ctrs2,self.mov_UL[1]))
        self.spinBoxSetA_6.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_6,ctrs2,self.mov_UL[2]))

        self.spinBoxSetA_7.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_7,ctrs1,self.mov_OR[0]))
        self.spinBoxSetA_8.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_8,ctrs1,self.mov_OR[1]))
        self.spinBoxSetA_9.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_9,ctrs1,self.mov_OR[2]))

        self.spinBoxSetA_10.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_10,ctrs1,self.mov_OC[0]))
        self.spinBoxSetA_11.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_11,ctrs1,self.mov_OC[1]))
        self.spinBoxSetA_12.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_12,ctrs1,self.mov_OC[2]))

        self.spinBoxSetA_13.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_13,ctrs2,self.mov_OL[0]))
        self.spinBoxSetA_14.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_14,ctrs2,self.mov_OL[1]))
        self.spinBoxSetA_15.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_15,ctrs2,self.mov_OL[2]))

        self.spinBoxSetA_16.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_16,ctrs1,self.mov_DR[0]))
        self.spinBoxSetA_17.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_17,ctrs1,self.mov_DR[1]))
        self.spinBoxSetA_18.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_18,ctrs1,self.mov_DR[2]))

        self.spinBoxSetA_19.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_19,ctrs2,self.mov_DL[0]))
        self.spinBoxSetA_20.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_20,ctrs2,self.mov_DL[1]))
        self.spinBoxSetA_21.valueChanged.connect(lambda:self.thread_chg_v_a(self.spinBoxSetA_21,ctrs2,self.mov_DL[2]))
        
        ###################################################################################
        #####################################tab Connection################################
        ###################################################################################

        self.connection_infos(ctrs1,'URP1') # CONTROLLER 1, CALLED 2
        self.connection_infos(ctrs1,'URP2') # CONTROLLER 2, CALLED 3
        self.connection_infos(ctrs1,'URP3') # CONTROLLER 3, CALLED 1

        self.connection_infos(ctrs2,'ULP1') # CONTROLLER 1, CALLED 3
        self.connection_infos(ctrs2,'ULP2') # CONTROLLER 2, CALLED 1
        self.connection_infos(ctrs2,'ULP3') # CONTROLLER 3, CALLED 2

        self.show()


    ###################################################################################################################
    ############################################### tab config#########################################################
    ###################################################################################################################
    
    ################ set ################

    def thread_chg_v_a(self,*args):

        spin_box, *_ =args

        if 'V' in spin_box.objectName():
            t_v_a = threading.Thread(target=self.set_v,args=(args))

        else:
            t_v_a = threading.Thread(target=self.set_a,args=(args))

        t_v_a.start()
        
    def set_v(self,spin_box_piezo,ctrsi_,piezos):

        ctr,piezo = piezos
        ctrsi = ctrsi_
        value = spin_box_piezo.value()

        # change velocity
        ctrsi.set_velocity(ctr,piezo,value)

        # uodate the label value
        self.infos(ctrsi,piezos)

    def set_a(self,spin_box_piezo,ctrsi_,piezos):

        ctr,piezo = piezos
        ctrsi = ctrsi_
        value = spin_box_piezo.value()
        
        # change acceleration
        ctrsi.set_acceleration(ctr,piezo,value)

        # update the label value
        self.infos(ctrsi,piezos)

    ################ get ################


    def v_between_callback(self,*args):

        ctrsi,ctr,piezo = args

        asyncio.set_event_loop(self.loop)

        velocity = self.loop.run_until_complete(self.axis_velocity(ctrsi,ctr,piezo))

        return velocity

    def a_between_callback(self,*args):

        ctrsi,ctr,piezo = args

        asyncio.set_event_loop(self.loop)

        acceleration = self.loop.run_until_complete(self.axis_acceleration(ctrsi,ctr,piezo))

        return acceleration

    async def axis_velocity(self,*args):

        # global velocity

        ctrsi,ctr,piezo = args

        ######
        await ctrsi.get_velocity(ctr,piezo)
        await ctrsi.get_velocity(ctr,piezo)

        velocity = await ctrsi.get_velocity(ctr,piezo)

        return velocity

    async def axis_acceleration(self,*args):

        # global acceleration

        ctrsi,ctr,piezo = args

        ######
        await ctrsi.get_acceleration(ctr,piezo)
        await ctrsi.get_acceleration(ctr,piezo)

        acceleration = await ctrsi.get_acceleration(ctr,piezo)

        return acceleration

    def infos(self,ctrsi,piezos):

        # global velocity
        
        dict_labels_v = {f'{ctrs1}:{self.mov_UR[0]}':self.labelVelocity,
                        f'{ctrs1}:{self.mov_UR[1]}':self.labelVelocity_2,
                        f'{ctrs1}:{self.mov_UR[2]}':self.labelVelocity_3,
                        
                        f'{ctrs2}:{self.mov_UL[0]}':self.labelVelocity_4,
                        f'{ctrs2}:{self.mov_UL[1]}':self.labelVelocity_5,
                        f'{ctrs2}:{self.mov_UL[2]}':self.labelVelocity_6,
                        
                        f'{ctrs1}:{self.mov_OR[0]}':self.labelVelocity_7,
                        f'{ctrs1}:{self.mov_OR[1]}':self.labelVelocity_8,
                        f'{ctrs1}:{self.mov_OR[2]}':self.labelVelocity_9,
                        
                        f'{ctrs1}:{self.mov_OC[0]}':self.labelVelocity_10,
                        f'{ctrs1}:{self.mov_OC[1]}':self.labelVelocity_11,
                        f'{ctrs1}:{self.mov_OC[2]}':self.labelVelocity_12,
                        
                        f'{ctrs2}:{self.mov_OL[0]}':self.labelVelocity_13, #
                        f'{ctrs2}:{self.mov_OL[1]}':self.labelVelocity_14,
                        f'{ctrs2}:{self.mov_OL[2]}':self.labelVelocity_15,
                        
                        f'{ctrs1}:{self.mov_DR[0]}':self.labelVelocity_17, #
                        f'{ctrs1}:{self.mov_DR[1]}':self.labelVelocity_16,
                        f'{ctrs1}:{self.mov_DR[2]}':self.labelVelocity_18,
                        
                        f'{ctrs2}:{self.mov_DL[0]}':self.labelVelocity_19,
                        f'{ctrs2}:{self.mov_DL[1]}':self.labelVelocity_20, #
                        f'{ctrs2}:{self.mov_DL[2]}':self.labelVelocity_21}
       

        dict_labels_a = {f'{ctrs1}:{self.mov_UR[0]}':self.labelAcceleration,
                        f'{ctrs1}:{self.mov_UR[1]}':self.labelAcceleration_2,
                        f'{ctrs1}:{self.mov_UR[2]}':self.labelAcceleration_3,
                        
                        f'{ctrs2}:{self.mov_UL[0]}':self.labelAcceleration_4,
                        f'{ctrs2}:{self.mov_UL[1]}':self.labelAcceleration_5,
                        f'{ctrs2}:{self.mov_UL[2]}':self.labelAcceleration_6,
                        
                        f'{ctrs1}:{self.mov_OR[0]}':self.labelAcceleration_7,
                        f'{ctrs1}:{self.mov_OR[1]}':self.labelAcceleration_8,
                        f'{ctrs1}:{self.mov_OR[2]}':self.labelAcceleration_9,
                        
                        f'{ctrs1}:{self.mov_OC[0]}':self.labelAcceleration_10,
                        f'{ctrs1}:{self.mov_OC[1]}':self.labelAcceleration_11,
                        f'{ctrs1}:{self.mov_OC[2]}':self.labelAcceleration_12,
                        
                        f'{ctrs2}:{self.mov_OL[0]}':self.labelAcceleration_13, #
                        f'{ctrs2}:{self.mov_OL[1]}':self.labelAcceleration_14,
                        f'{ctrs2}:{self.mov_OL[2]}':self.labelAcceleration_15,
                        
                        f'{ctrs1}:{self.mov_DR[0]}':self.labelAcceleration_16, #
                        f'{ctrs1}:{self.mov_DR[1]}':self.labelAcceleration_17,
                        f'{ctrs1}:{self.mov_DR[2]}':self.labelAcceleration_18,
                        
                        f'{ctrs2}:{self.mov_DL[0]}':self.labelAcceleration_19,
                        f'{ctrs2}:{self.mov_DL[1]}':self.labelAcceleration_20, #
                        f'{ctrs2}:{self.mov_DL[2]}':self.labelAcceleration_21}

        ctr,piezo = piezos
        
        thread_axis_v = threading.Thread(target = lambda q,ctrsi,ctr,piezo: q.put(self.v_between_callback(ctrsi,ctr,piezo)),args=(self.queue_axis_v,ctrsi,ctr,piezo))
        thread_axis_v.start()
        thread_axis_v.join()

        # thread_axis_a = threading.Thread(target =self.a_between_callback,args=(ctrsi,ctr,piezo))
        thread_axis_a = threading.Thread(target =lambda q,ctrsi,ctr,piezo: q.put(self.a_between_callback(ctrsi,ctr,piezo)),args=(self.queue_axis_a,ctrsi,ctr,piezo))
        thread_axis_a.start()
        thread_axis_a.join()

        # dict_labels_v[f'{ctrsi}:{piezos}'].setText(str(velocity))
        # dict_labels_a[f'{ctrsi}:{piezos}'].setText(str(acceleration))

        dict_labels_v[f'{ctrsi}:{piezos}'].setText(str(self.queue_axis_v.get()))
        dict_labels_a[f'{ctrsi}:{piezos}'].setText(str(self.queue_axis_a.get()))

    ###################################################################################################################
    ############################################### general tab #######################################################
    ###################################################################################################################

    async def finished(self,*args):
        
        # print(args)

        # _,
        ctrsi,ctr,piezo = args
        # yo = 0
        # print(ctrsi,ctr,piezo)
        # while yo !=1:

        #     yo = await ctrsi.finish(ctr,piezo)
        flag_movement = await ctrsi.finish(ctr,piezo)

        # print(f'yo:{yo}')

        # no movement in progress
        # self.flag_movement.put(True)
        return True
        # try:
            
        #     yo = await ctrsi.finish(ctr,piezo)
        #     return yo

        # # except RuntimeError:
        # except:
        #     print('Another movement in progress.')


    def between_callback(self,*args):

        ctrsi,ctr,piezo,led = args

        # print(args)

        # try:
        # set movement icon: red
        led.setPixmap(QtGui.QPixmap(icon_red_led))

        asyncio.set_event_loop(self.loop)
        self.flag_movement = self.loop.run_until_complete(self.finished(ctrsi,ctr,piezo))
        # print(f'flag_movement:{self.flag_movement}')
        # set movement icon: green
        led.setPixmap(QtGui.QPixmap(icon_green_led))
        # except:
        # #  RuntimeError:
        #     print('Another movement in progress.')

        # return flag_movement

    def exec_movement_all(self,button):

        # movement in progress
        # self.flag_movement.put(False)   

        self.abort = False
        ############################
        # controller group 1: ctrs1#
        ############################        
        
        # MOVE UR
        if button == self.pushButtonGoURm or button == self.pushButtonGoURp:

            piezos = self.mov_UR
            ctrsi = ctrs1
            steps = [self.spinBoxStepsURP1.value(),self.spinBoxStepsURP2.value(), self.spinBoxStepsURP3.value()]
            loops = self.spinBoxLoopsUR.value() 
            led = self.labelLedUR
            
        # MOVE OR
        elif button == self.pushButtonGoORm or button == self.pushButtonGoORp:
            
            piezos = self.mov_OR
            ctrsi = ctrs1
            steps = [self.spinBoxStepsORP1.value(),self.spinBoxStepsORP2.value(), self.spinBoxStepsORP3.value()]
            loops = self.spinBoxLoopsOR.value()
            led = self.labelLedOR
        
        # MOVE DR
        elif button == self.pushButtonGoDRm or button == self.pushButtonGoDRp:
            
            piezos = self.mov_DR
            ctrsi = ctrs1
            steps = [self.spinBoxStepsDRP1.value(),self.spinBoxStepsDRP2.value(), self.spinBoxStepsDRP3.value()]
            loops = self.spinBoxLoopsDR.value()
            led = self.labelLedDR

        # MOVE OC
        elif button == self.pushButtonGoOCm or button == self.pushButtonGoOCp:
                
            piezos = self.mov_OC
            ctrsi = ctrs1
            steps = [self.spinBoxStepsOCP1.value(),self.spinBoxStepsOCP2.value(), self.spinBoxStepsOCP3.value()]
            loops = self.spinBoxLoopsOC.value()
            led = self.labelLedOC
            

        ############################
        # controller group 2: ctrs2#
        ############################        
        
        # MOVE UL
        elif button == self.pushButtonGoULm or button == self.pushButtonGoULp:
            
            piezos = self.mov_UL
            ctrsi = ctrs2
            steps = [self.spinBoxStepsULP1.value(),self.spinBoxStepsULP2.value(), self.spinBoxStepsULP3.value()]
            loops = self.spinBoxLoopsUL.value()
            led = self.labelLedUL
        
        # MOVE OL
        elif button == self.pushButtonGoOLm or button == self.pushButtonGoOLp:
            
            piezos = self.mov_OL
            ctrsi = ctrs2
            steps = [self.spinBoxStepsOLP1.value(),self.spinBoxStepsOLP2.value(), self.spinBoxStepsOLP3.value()]
            loops = self.spinBoxLoopsOL.value()
            led = self.labelLedOL
            
        
        # MOVE DL
        elif button == self.pushButtonGoDLm or button == self.pushButtonGoDLp:
    
            piezos = self.mov_DL
            ctrsi = ctrs2
            steps = [self.spinBoxStepsDLP1.value(),self.spinBoxStepsDLP2.value(), self.spinBoxStepsDLP3.value()]
            loops = self.spinBoxLoopsDL.value()
            led = self.labelLedDL
            
        
        for cicle in range(loops):
            for piezo_i,step in zip(piezos,steps):

                ctr,piezo = piezo_i
                ctrsi.set_relative(ctr,piezo,step)

                print(f'Sending {cicle} instruction for {piezos}')


                _thread = threading.Thread(target=self.between_callback, args=(ctrsi,ctr,piezo,led))
                _thread.start()
                _thread.join()
                
                if self.abort == True:
                    break
            if self.abort == True:
                break

    def thread_go_all(self,button):

        # self.pushButtonResetAll.setText('Reset All')

        # if self.flag_movement.get():
        if self.flag_movement:

            # t1 = threading.Thread(target=lambda q, button: q.put(self.exec_movement_all(button)),args=(self.flag_movement,button))
            t1 = threading.Thread(target=self.exec_movement_all,args=(button,))
            t1.start()
            self.flag_movement = False
        # except RuntimeError:
        else:
            print('Another movement in progress.')
    
    def exec_movement(self,button):

        # movement in progress
        self.abort = False

        ############################
        # controller group 1: ctrs1#
        ############################        
        
        # MOVE UR
        if button == self.pushButtonGoURP1m or button == self.pushButtonGoURP1p:

            piezos = self.mov_UR[0]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsURP1.value()

            if button ==self.pushButtonGoURP1m:
                steps = -steps

            loops = self.spinBoxLoopsUR.value()
            led = self.labelLedUR
        
        elif button == self.pushButtonGoURP2m or button == self.pushButtonGoURP2p:

            piezos = self.mov_UR[1]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsURP2.value()

            if button == self.pushButtonGoURP2m:
                steps=-steps

            loops = self.spinBoxLoopsUR.value()
            led = self.labelLedUR
        
        elif button == self.pushButtonGoURP3m or button == self.pushButtonGoURP3p:

            piezos = self.mov_UR[2]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsURP3.value()

            if button == self.pushButtonGoURP3m:
                steps = -steps

            loops = self.spinBoxLoopsUR.value()
            led = self.labelLedUR

        # MOVE OR
        elif button == self.pushButtonGoORP1m or button == self.pushButtonGoORP1p:
            
            piezos = self.mov_OR[0]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsORP1.value()

            if button == self.pushButtonGoORP1m:
                steps = -steps

            loops = self.spinBoxLoopsOR.value()
            led = self.labelLedOR

        elif button == self.pushButtonGoORP2m or button == self.pushButtonGoORP2p:
            
            piezos = self.mov_OR[1]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsORP2.value()

            if button == self.pushButtonGoORP2m:
                steps = -steps

            loops = self.spinBoxLoopsOR.value()
            led = self.labelLedOR
        
        elif button == self.pushButtonGoORP3m or button == self.pushButtonGoORP3p:
            
            piezos = self.mov_OR[2]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsORP3.value()

            if button == self.pushButtonGoORP3m:
                steps = -steps

            loops = self.spinBoxLoopsOR.value()
            led = self.labelLedOR
        
        # MOVE DR
        elif button == self.pushButtonGoDRP1m or button == self.pushButtonGoDRP1p:
            
            piezos = self.mov_DR[0]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsDRP1.value()

            if button == self.pushButtonGoDRP1m:
                steps = -steps

            loops = self.spinBoxLoopsDR.value()
            led = self.labelLedDR

        elif button == self.pushButtonGoDRP2m or button == self.pushButtonGoDRP2p:
            
            piezos = self.mov_DR[1]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsDRP2.value()
            
            if button == self.pushButtonGoDRP2p:
                steps = -steps

            loops = self.spinBoxLoopsDR.value()
            led = self.labelLedDR
        
        elif button == self.pushButtonGoDRP3m or button == self.pushButtonGoDRP3p:
            
            piezos = self.mov_DR[2]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsDRP3.value()

            if button == self.pushButtonGoDRP3m:
                steps = -steps

            loops = self.spinBoxLoopsDR.value()
            led = self.labelLedDR

        # MOVE OC
        elif button == self.pushButtonGoOCP1m or button == self.pushButtonGoOCP1p:
                
            piezos = self.mov_OC[0]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsOCP1.value()

            if button == self.pushButtonGoOCP1m:
                steps = -steps

            loops = self.spinBoxLoopsOC.value()
            led = self.labelLedOC
        
        elif button == self.pushButtonGoOCP2m or button == self.pushButtonGoOCP2p:
                
            piezos = self.mov_OC[1]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsOCP2.value()
            
            if button == self.pushButtonGoOCP2m:
                steps = -steps

            loops = self.spinBoxLoopsOC.value()
            led = self.labelLedOC
        
        elif button == self.pushButtonGoOCP3m or button == self.pushButtonGoOCP3p:
                
            piezos = self.mov_OC[2]
            # ctrsi = self.ctrs1
            ctrsi = ctrs1
            steps = self.spinBoxStepsOCP3.value()

            if button == self.pushButtonGoOCP3m:
                steps=-steps

            loops = self.spinBoxLoopsOC.value()
            led = self.labelLedOC
            

        ############################
        # controller group 2: ctrs2#
        ############################        
        
        # MOVE UL
        elif button == self.pushButtonGoULP1m or button == self.pushButtonGoULP1p:
            
            piezos = self.mov_UL[0]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsULP1.value()

            if button == self.pushButtonGoULP1m:
                steps = -steps
            loops = self.spinBoxLoopsUL.value()
            led = self.labelLedUL
        
        elif button == self.pushButtonGoULP2m or button == self.pushButtonGoULP2p:
            
            piezos = self.mov_UL[1]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsULP2.value()

            if button == self.pushButtonGoULP2m:
                steps = -steps

            loops = self.spinBoxLoopsUL.value()
            led = self.labelLedUL
        
        elif button == self.pushButtonGoULP3m or button == self.pushButtonGoULP3p:
            
            piezos = self.mov_UL[2]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsULP3.value()

            if button == self.pushButtonGoULP3m:
                steps = -steps

            loops = self.spinBoxLoopsUL.value()
            led = self.labelLedUL
        
        # MOVE OL
        elif button == self.pushButtonGoOLP1m or button == self.pushButtonGoOLP1p:
            
            piezos = self.mov_OL[0]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsOLP1.value()

            if button == self.pushButtonGoOLP1m:
                steps = -steps

            loops = self.spinBoxLoopsOL.value()
            led = self.labelLedOL
        
        elif button == self.pushButtonGoOLP2m or button == self.pushButtonGoOLP2p:
            
            piezos = self.mov_OL[1]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsOLP2.value()

            if button == self.pushButtonGoOLP2m:
                steps = -steps

            loops = self.spinBoxLoopsOL.value()
            led = self.labelLedOL

        elif button == self.pushButtonGoOLP3m or button == self.pushButtonGoOLP3p:
            
            piezos = self.mov_OL[2]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsOLP3.value()

            if button == self.pushButtonGoOLP3m:
                steps = -steps

            loops = self.spinBoxLoopsOL.value()
            led = self.labelLedOL
        
        # MOVE DL
        elif button == self.pushButtonGoDLP1m or button == self.pushButtonGoDLP1p:
    
            piezos = self.mov_DL[0]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsDLP1.value()

            if button == self.pushButtonGoDLP1m:
                steps = -steps

            loops = self.spinBoxLoopsDL.value()
            led = self.labelLedDL

        elif button == self.pushButtonGoDLP2m or button == self.pushButtonGoDLP2p:
    
            piezos = self.mov_DL[1]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsDLP2.value()

            if button == self.pushButtonGoDLP2m:
                steps = -steps

            loops = self.spinBoxLoopsDL.value()
            led = self.labelLedDL

        elif button == self.pushButtonGoDLP3m or button == self.pushButtonGoDLP3p:
    
            piezos = self.mov_DL[2]
            # ctrsi = self.ctrs2
            ctrsi = ctrs2
            steps = self.spinBoxStepsDLP3.value()

            if button == self.pushButtonGoDLP3m:

                steps = -steps

            loops = self.spinBoxLoopsDL.value()
            led = self.labelLedDL
            

        for cicle in range(loops):

            ctr,piezo = piezos
            ctrsi.set_relative(ctr,piezo,steps)
            
            print(f'Sending {cicle} instruction for {piezos}')

            _thread = threading.Thread(target=self.between_callback,args=(ctrsi,ctr,piezo,led))
            _thread.start()
            _thread.join()

            if self.abort == True:
                break
        
    def thread(self,button):

        if self.flag_movement:

            t1 = threading.Thread(target= self.exec_movement,args=(button,))
            t1.start()
            self.flag_movement = False
        else:
            print('Another movement in progress.')

    def abort_mov(self,button):

        ################################################
        ### abort motion in controller group 1: ctrs1###
        ################################################

        if button == self.pushButtonAbortUR:
            ctrs1.abort(2,1)
            ctrs1.abort(3,1)
            ctrs1.abort(1,1)

        elif button == self.pushButtonAbortOR:
            ctrs1.abort(2,2)
            ctrs1.abort(3,2)
            ctrs1.abort(1,2)
        
        elif button == self.pushButtonAbortDR:
            ctrs1.abort(2,3)
            ctrs1.abort(3,3)
            ctrs1.abort(1,3)

        elif button == self.pushButtonAbortOC:
            ctrs1.abort(2,4)
            ctrs1.abort(3,4)
            ctrs1.abort(1,4)
        
        ################################################
        ### abort motion in controller group 2: ctrs2###
        ################################################

        elif button == self.pushButtonAbortUL:
            ctrs2.abort(2,1)
            ctrs2.abort(3,1)
            ctrs2.abort(1,1)

        elif button == self.pushButtonAbortOL:
            ctrs2.abort(2,2)
            ctrs2.abort(3,2)
            ctrs2.abort(1,2)
        
        elif button == self.pushButtonAbortDL:
            ctrs2.abort(2,3) #p2
            ctrs2.abort(3,3)
            ctrs2.abort(1,3)
        
        self.abort=True

    def reset_controlers(self):

        self.pushButtonResetAll.setText('Reseted')

        ctrs1.reset(1)
        ctrs1.reset(2)
        ctrs1.reset(3)
        ctrs2.reset(1)
        ctrs2.reset(2)
        ctrs2.reset(3)

        print('Controlers reseted.')

        self.close()

    ###################################################################################################################
    ############################################### tab connection #########################################################
    ###################################################################################################################

    ################ infos por controlador ################

    async def controller_infos(self,*args):

        ctrsi,ctr= args

        n_id = 0
        while n_id != 5:
            identification = await ctrsi.identify(ctr)
            n_id = len(identification.split(' '))

        gateway = '0'
        while '192' not in gateway:
            gateway = await ctrsi.get_gateway(ctr)

        n_host = 0
        while n_host != 2:

            hostname = await ctrsi.get_hostname(ctr)
            n_host = len(hostname.split('-'))

        n_mac = 0
        while n_mac !=2:
            mac = await ctrsi.get_mac(ctr)
            n_mac = len(mac.split(', '))

        n_ipaddr = 0
        while n_ipaddr !=4:

            ipaddr = await ctrsi.get_ip(ctr)
            n_ipaddr = len(ipaddr.split('.'))

        return identification, gateway, hostname, mac, ipaddr

    def info_between_callback(self,*args):

        ctrsi,ctr = args

        asyncio.set_event_loop(self.loop)

        # identification, gateway, hostname, mac, ipaddr = 
        net_infos = self.loop.run_until_complete(self.controller_infos(ctrsi,ctr))

        return net_infos

    def connection_infos(self,ctrsi,favo_piezo):

        dict_connection = {
            'URP1':[2,self.labelPiezos,self.labelModelName,self.labelFirmwareVN,self.labelFirmwareBD,
                    self.labelControllerSN,self.labelGateway,self.labelIp,self.labelHostname,self.labelMac,'P1: UR,OR,DR,OC'],

            'URP2':[3,self.labelPiezos_2,self.labelModelName_2,self.labelFirmwareVN_2,self.labelFirmwareBD_2,
                    self.labelControllerSN_2,self.labelGateway_2,self.labelIp_2,self.labelHostname_2,self.labelMac_2,'P2: UR,OR,DR,OC'],

            'URP3':[1,self.labelPiezos_3,self.labelModelName_3,self.labelFirmwareVN_3,self.labelFirmwareBD_3,
                    self.labelControllerSN_3,self.labelGateway_3,self.labelIp_3,self.labelHostname_3,self.labelMac_3,'P3: UR,OR,DR,OC'],

            'ULP1':[3,self.labelPiezos_5,self.labelModelName_5,self.labelFirmwareVN_5,self.labelFirmwareBD_5,
                    self.labelControllerSN_5,self.labelGateway_5,self.labelIp_5,self.labelHostname_5,self.labelMac_5,'P1: UL,OL,DL'],
            'ULP2':[1,self.labelPiezos_6,self.labelModelName_6,self.labelFirmwareVN_6,self.labelFirmwareBD_6,
                    self.labelControllerSN_6,self.labelGateway_6,self.labelIp_6,self.labelHostname_6,self.labelMac_6,'P2: UL,OL,DL'],
            'ULP3':[2,self.labelPiezos_4,self.labelModelName_4,self.labelFirmwareVN_4,self.labelFirmwareBD_4,
                    self.labelControllerSN_4,self.labelGateway_4,self.labelIp_4,self.labelHostname_4,self.labelMac_4,'P3: UL,OL,DL'],
        }

        thread_con_info = threading.Thread(target=lambda q,ctrsi,dict_connection: q.put(self.info_between_callback(ctrsi,dict_connection)),args=(self.queue_axis_infos,ctrsi,dict_connection[favo_piezo][0]))
        thread_con_info.start()
        thread_con_info.join()

        a = self.queue_axis_infos.get()
        identification, gateway, mac, hostname, ipaddr = a

        dict_connection[favo_piezo][1].setText(dict_connection[favo_piezo][10])
        _,model_name, fw_version,fw_date,ctr_serial = identification.split(' ')

        dict_connection[favo_piezo][2].setText(f'Model Name: {model_name}')
        dict_connection[favo_piezo][3].setText(f'Firmware version number: {fw_version}')
        dict_connection[favo_piezo][4].setText(f'Firmware build date: {fw_date}')
        dict_connection[favo_piezo][5].setText(f'Controller serial number: {ctr_serial}')

        dict_connection[favo_piezo][6].setText(f'Gateway: {gateway}')
        dict_connection[favo_piezo][7].setText(f'Ip: {ipaddr}')
        dict_connection[favo_piezo][8].setText(f'Hostname: {hostname}')
        dict_connection[favo_piezo][9].setText(f'Mac: {mac}')


async def con_tcp():

    global ctrs1,ctrs2

    ctrs1 = await tcp.connect('8742-44513')
    ctrs2 = await tcp.connect('8742-42177')
    print('Connected')

    return [ctrs1,ctrs2]

def start_connection(loop):
    loop.run_until_complete(con_tcp())

def main():

    loop = asyncio.get_event_loop()
    
    global app

    app = QtWidgets.QApplication(sys.argv)

    

    thread_tcp = threading.Thread(target=start_connection,args=(loop,))
    thread_tcp.start()
    thread_tcp.join()

    window = GuiPiezos(loop=loop)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
