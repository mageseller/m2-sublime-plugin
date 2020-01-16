import sublime, sublime_plugin
import os
import re

class MagentoCreateModuleCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("New Module:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        regex = re.compile("([a-zA-Z0-9]*)_([a-zA-Z0-9]*)")
        folder_path =  self.window.active_view().window().folders();
        if (regex.match(text) != None):
            text_split = text.split("_");
            namespace = text_split[0];
            moduleName = text_split[1];
           
            path = os.path.join(folder_path[0], 'app', 'code', namespace, moduleName );
            
            
            # Create folder structure
            os.makedirs(path)
            os.makedirs(os.path.join(path, 'etc','frontend'))
            os.makedirs(os.path.join(path, 'Model'))
            os.makedirs(os.path.join(path, 'Block'))
            os.makedirs(os.path.join(path, 'Controller'))
            os.makedirs(os.path.join(path, 'view','frontend'))

            self.create_registration(path, namespace, moduleName)
            self.create_etc_modules_xml(path, namespace, moduleName)
            binmagento = os.path.join(folder_path[0],'bin','magento')
            commadString = 'php ' + binmagento+' module:enable '+namespace+'_'+moduleName
            print(commadString)

            myCmd = os.popen(commadString).read()
            print(myCmd)


            #os.system('php ' + binmagento+' module:enable '+namespace+'_'+moduleName)

            
        pass


    def create_registration(self, path, namespace, moduleName):
        template = """<?php
\\Magento\\Framework\\Component\\ComponentRegistrar::register(
    \\Magento\\Framework\\Component\\ComponentRegistrar::MODULE,
    '{namespace}_{moduleName}',
    __DIR__
);
        """
        data = {"namespace" : namespace,
                "moduleName" : moduleName}
        file = open(os.path.join(path, 'registration.php'), 'w+')
        file.write(template.format(**data))


    def create_etc_modules_xml(self, path, namespace, moduleName):
        template = """<?xml version="1.0" ?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="{namespace}_{moduleName}" setup_version="1.0.0">
        <sequence>
            <module name="Magento_Sales"/>
        </sequence>
    </module>
</config>"""
        data = {"namespace" : namespace,
                "moduleName" : moduleName}
        file = open(os.path.join(path,'etc','module.xml'), 'w+')
        file.write(template.format(**data))        
        pass

