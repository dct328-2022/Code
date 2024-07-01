
class WriteCpp:
    def __init__(self, path):
        self.path = path

    def path(self):
        return path

    def WriteCommands(self):
        content = open(self.path, 'w')
        for header in Domain.instances[0].include():
            content.write('#include <%s>\n' % header)

        # write node header files
        if len(Node.instances) > 0:
            for header in Node.instances[0].include():
                content.write('#include <%s>\n' % header)

        if len(Vector.instances) > 0:
            for header in Vector.instances[0].include():
                content.write('#include <%s>\n' % header)

        # write Constraint header files
        if len(SPConstraint.instances) > 0:
            for header in SPConstraint.instances[0].include():
                content.write('#include <%s>\n' % header)

        # write Constraint header files
        if len(MPConstraint.instances) > 0:
            for header in MPConstraint.instances[0].include():
                content.write('#include <%s>\n' % header)

        # write geometric transformation header files
        if GeometricTransformation.Counter > 0:
            for header in GeometricTransformation.instances[0].include():
                content.write('#include <%s>\n' % header)

        # write uniaxial material header files
        if len(uniaxialMaterial.instances) > 0:
            commandtemp = []
            for instance in uniaxialMaterial.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(NDMaterial.instances) > 0:
            commandtemp = []
            for instance in NDMaterial.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(Friction.instances) > 0:
            commandtemp = []
            for instance in Friction.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(Fiber.instances) > 0:
            commandtemp = []
            for instance in Fiber.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(Section.instances) > 0:
            commandtemp = []
            for instance in Section.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(BeamIntegration.instances) > 0:
            commandtemp = []
            for instance in BeamIntegration.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(LineElement.instances) > 0:
            commandtemp = []
            for instance in LineElement.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(ShellElement.instances) > 0:
            commandtemp = []
            for instance in ShellElement.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(TimeSeries.instances) > 0:
            commandtemp = []
            for instance in TimeSeries.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(Recorder.instances) > 0:
            commandtemp = []
            for instance in Recorder.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(LoadPattern.instances) > 0:
            commandtemp = []
            for instance in LoadPattern.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(Load.instances) > 0:
            commandtemp = []
            for instance in Load.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(GroundMotion.instances) > 0:
            commandtemp = []
            for instance in GroundMotion.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(ImposedMotion.instances) > 0:
            commandtemp = []
            for instance in ImposedMotion.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)

        if len(AnalysisOption.instances) > 0:
            commandtemp = []
            for instance in AnalysisOption.instances:
                for header in instance.include():
                    if header not in commandtemp:
                        commandtemp.append(header)
                        content.write('#include <%s>\n' % header)


        content.write('\n')
        content.write('StandardStream sserr;\nOPS_Stream *opserrPtr = &sserr;\n')
        content.write('int main(int argc, char **argv) {\n\n')

        for instance in Domain.instances:
            for command in instance.command:
                content.write('%s' % command)

        content.write('\n')

        if len(Node.instances) > 0:
            for instance in Node.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(Vector.instances) > 0:
            for instance in Vector.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(SPConstraint.instances) > 0:
            for instance in SPConstraint.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(MPConstraint.instances) > 0:
            for instance in MPConstraint.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(GeometricTransformation.instances) > 0:
            for instance in GeometricTransformation.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(uniaxialMaterial.instances) > 0:
            for instance in uniaxialMaterial.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(NDMaterial.instances) > 0:
            for instance in NDMaterial.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(Friction.instances) > 0:
            for instance in Friction.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(Fiber.instances) > 0:
            for instance in Fiber.instances:
                content.write('%s' % instance.command)

        if len(Section.instances) > 0:
            for instance in Section.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(BeamIntegration.instances) > 0:
            for instance in BeamIntegration.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(LineElement.instances) > 0:
            for instance in LineElement.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(ShellElement.instances) > 0:
            for instance in ShellElement.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(TimeSeries.instances) > 0:
            for instance in TimeSeries.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(Recorder.instances) > 0:
            for instance in Recorder.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(LoadPattern.instances) > 0:
            for instance in LoadPattern.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(GroundMotion.instances) > 0:
            for instance in GroundMotion.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(ImposedMotion.instances) > 0:
            for instance in ImposedMotion.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(Load.instances) > 0:
            for instance in Load.instances:
                content.write('%s' % instance.command)

        content.write('\n')

        if len(AnalysisOption.instances) > 0:
            for instance in AnalysisOption.instances:
                content.write('%s' % instance.command)

        content.write('\n')
        content.write('exit(0);\n')
        content.write("\n")
        content.write('}')

        print("Nodes: %d\n" % len(Node.instances))



