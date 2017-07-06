'''
testing some stuff
'''

# from content import Content
# 
# process_list ='/dls/science/users/clb02321/DAWN_stable/Savu/Savu/test_data/test_process_lists/pymca_test.nxs'
# model = Content()
# model.fopen(process_list)
# model.modify('1', 'x', 'cheese')

# class ControllerFactory(object):
#     def __init__(self, model, plugin_number, key, widget):
#         self.model = model
#         self.plugin_number = plugin_number
#         self.key = key
#         self.widget = widget
#     
#     def controller(self):
#         widgetvalue = str(self.widget.value())
# #         print "wv", widgetvalue
#         self.model.modify(self.plugin_number, self.key, widgetvalue)



# def get_visits():
# 
#     import getpass
#     from subprocess import Popen, PIPE
#     
#     p = Popen(['sh','/dls_sw/apps/mx-scripts/visit_tools/getVisitsForFedId',getpass.getuser()], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#     output, err = p.communicate(b"input data that is passed to subprocess' stdin")
#     rc = p.returncode
#     return output

def get_current_visit():
    import os
    from subprocess import Popen, PIPE,call
#     p = call(['sh','/dls_sw/apps/mx-scripts/visit_tools/currentvisit','$BEAMLINE'])
    p = Popen(['sh','/dls_sw/apps/mx-scripts/visit_tools/currentvisit',os.environ["BEAMLINE"]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    return output
    
if __name__ == "__main__":
    get_current_visit()