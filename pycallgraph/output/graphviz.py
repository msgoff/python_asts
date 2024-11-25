from __future__ import division

import tempfile
import os
import textwrap
import subprocess as sub


class Output(object):
    """Base class for all outputters."""

    def __init__(self, **kwargs):
        self.node_color_func = self.node_color
        self.edge_color_func = self.edge_color
        self.node_label_func = self.node_label
        self.edge_label_func = self.edge_label

        # Update the defaults with anything from kwargs
        [setattr(self, k, v) for k, v in kwargs.items()]

    def set_config(self, config):
        """
        This is a quick hack to move the config variables set in Config into
        the output module config variables.
        """
        for k, v in config.__dict__.items():
            if hasattr(self, k) and callable(getattr(self, k)):
                continue
            setattr(self, k, v)

    def node_color(self, node):
        value = float(node.time.fraction * 2 + node.calls.fraction) / 3
        return Color.hsv(value / 2 + 0.5, value, 0.9)

    def edge_color(self, edge):
        value = float(edge.time.fraction * 2 + edge.calls.fraction) / 3
        return Color.hsv(value / 2 + 0.5, value, 0.7)

    def node_label(self, node):
        parts = [
            "{0.name}",
            "calls: {0.calls.value:n}",
            "time: {0.time.value:f}s",
        ]

        if self.processor.config.memory:
            parts += [
                "memory in: {0.memory_in.value_human_bibyte}",
                "memory out: {0.memory_out.value_human_bibyte}",
            ]

        return r"\n".join(parts).format(node)

    def edge_label(self, edge):
        return "{0}".format(edge.calls.value)

    def sanity_check(self):
        """Basic checks for certain libraries or external applications.  Raise
        or warn if there is a problem.
        """
        pass

    @classmethod
    def add_arguments(cls, subparsers):
        pass

    def reset(self):
        pass

    def set_processor(self, processor):
        self.processor = processor

    def start(self):
        """Initialise variables after initial configuration."""
        pass

    def update(self):
        """Called periodically during a trace, but only when should_update is
        set to True.
        """
        raise NotImplementedError("update")

    def should_update(self):
        """Return True if the update method should be called periodically."""
        return False

    def done(self):
        """Called when the trace is complete and ready to be saved."""
        raise NotImplementedError("done")

    def ensure_binary(self, cmd):
        if find_executable(cmd):
            return

        raise PyCallGraphException(
            'The command "{0}" is required to be in your path.'.format(cmd)
        )

    def normalize_path(self, path):
        regex_user_expand = re.compile(r"\A~")
        if regex_user_expand.match(path):
            path = os.path.expanduser(path)
        else:
            path = os.path.expandvars(path)  # expand, just in case
        return path

    def prepare_output_file(self):
        if self.fp is None:
            self.output_file = self.normalize_path(self.output_file)
            self.fp = open(self.output_file, "wb")

    def verbose(self, text):
        self.processor.config.log_verbose(text)

    def debug(self, text):
        self.processor.config.log_debug(text)

    @classmethod
    def add_output_file(cls, subparser, defaults, help):
        subparser.add_argument(
            "-o",
            "--output-file",
            type=str,
            default=defaults.output_file,
            help=help,
        )


class Color(object):
    def __init__(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.validate_all()

    @classmethod
    def hsv(cls, h, s, v, a=1):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return cls(r, g, b, a)

    def __str__(self):
        return "<Color {}>".format(self.rgba_web())

    def validate_all(self):
        self.validate("r")
        self.validate("g")
        self.validate("b")
        self.validate("a")

    def validate(self, attr):
        v = getattr(self, attr)
        if not 0 <= v <= 1:
            raise ColorException("{} out of range 0 to 1: {}".format(attr, v))

    @property
    def r255(self):
        return int(self.r * 255)

    @property
    def g255(self):
        return int(self.g * 255)

    @property
    def b255(self):
        return int(self.b * 255)

    @property
    def a255(self):
        return int(self.a * 255)

    def rgb_web(self):
        """Returns a string with the RGB components as a HTML hex string."""
        return "#{0.r255:02x}{0.g255:02x}{0.b255:02x}".format(self)

    def rgba_web(self):
        """Returns a string with the RGBA components as a HTML hex string."""
        return "{0}{1.a255:02x}".format(self.rgb_web(), self)

    def rgb_csv(self):
        """Returns a string with the RGB components as CSV."""
        return "{0.r255},{0.g255},{0.b255}".format(self)


class PyCallGraphException(Exception):
    pass


class GraphvizOutput(Output):
    def __init__(self, **kwargs):
        self.tool = "dot"
        self.output_file = "pycallgraph.png"
        self.output_type = "png"
        self.font_name = "Verdana"
        self.font_size = 7
        self.group_font_size = 10
        self.group_border_color = Color(0, 0, 0, 0.8)

        Output.__init__(self, **kwargs)

        self.prepare_graph_attributes()

    @classmethod
    def add_arguments(cls, subparsers, parent_parser, usage):
        defaults = cls()

        subparser = subparsers.add_parser(
            "graphviz",
            help="Graphviz generation",
            parents=[parent_parser],
            usage=usage,
        )

        subparser.add_argument(
            "-l",
            "--tool",
            dest="tool",
            default=defaults.tool,
            help="The tool from Graphviz to use, e.g. dot, neato, etc.",
        )

        cls.add_output_file(subparser, defaults, "The generated Graphviz file")

        subparser.add_argument(
            "-f",
            "--output-format",
            type=str,
            default=defaults.output_type,
            dest="output_type",
            help="Image format to produce, e.g. png, ps, dot, etc. "
            "See http://www.graphviz.org/doc/info/output.html for more.",
        )

        subparser.add_argument(
            "--font-name",
            type=str,
            default=defaults.font_name,
            help="Name of the font to be used",
        )

        subparser.add_argument(
            "--font-size",
            type=int,
            default=defaults.font_size,
            help="Size of the font to be used",
        )

    def sanity_check(self):
        self.ensure_binary(self.tool)

    def prepare_graph_attributes(self):
        generated_message = "\\n".join(
            [
                r"Generated by Python Call Graph v%s" % "1.0.1",
                r"http://pycallgraph.slowchop.com",
            ]
        )

        self.graph_attributes = {
            "graph": {
                "overlap": "scalexy",
                "fontname": self.font_name,
                "fontsize": self.font_size,
                "fontcolor": Color(0, 0, 0, 0.5).rgba_web(),
                "label": generated_message,
            },
            "node": {
                "fontname": self.font_name,
                "fontsize": self.font_size,
                "fontcolor": Color(0, 0, 0).rgba_web(),
                "style": "filled",
                "shape": "rect",
            },
            "edge": {
                "fontname": self.font_name,
                "fontsize": self.font_size,
                "fontcolor": Color(0, 0, 0).rgba_web(),
            },
        }

    def done(self):
        source = self.generate()

        self.debug(source)

        fd, temp_name = tempfile.mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write(source)

        cmd = '"{0}" -T{1} -o{2} {3}'.format(
            self.tool, self.output_type, self.output_file, temp_name
        )

        self.verbose("Executing: {0}".format(cmd))
        try:
            proc = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
            ret, output = proc.communicate()
            if ret:
                raise PyCallGraphException(
                    'The command "%(cmd)s" failed with error '
                    "code %(ret)i." % locals()
                )
        finally:
            os.unlink(temp_name)

        self.verbose(
            "Generated {0} with {1} nodes.".format(
                self.output_file,
                len(self.processor.func_count),
            )
        )

    def generate(self):
        """Returns a string with the contents of a DOT file for Graphviz to
        parse.
        """
        indent_join = "\n" + " " * 12

        return textwrap.dedent(
            """\
        digraph G {{

            // Attributes
            {0}

            // Groups
            {1}

            // Nodes
            {2}

            // Edges
            {3}

        }}
        """.format(
                indent_join.join(self.generate_attributes()),
                indent_join.join(self.generate_groups()),
                indent_join.join(self.generate_nodes()),
                indent_join.join(self.generate_edges()),
            )
        )

    def attrs_from_dict(self, d):
        output = []
        for attr, val in d.items():
            output.append('%s = "%s"' % (attr, val))
        return ", ".join(output)

    def node(self, key, attr):
        return '"{0}" [{1}];'.format(
            key,
            self.attrs_from_dict(attr),
        )

    def edge(self, edge, attr):
        return '"{0.src_func}" -> "{0.dst_func}" [{1}];'.format(
            edge,
            self.attrs_from_dict(attr),
        )

    def generate_attributes(self):
        output = []
        for section, attrs in self.graph_attributes.items():
            output.append(
                "{0} [ {1} ];".format(
                    section,
                    self.attrs_from_dict(attrs),
                )
            )
        return output

    def generate_groups(self):
        if not self.processor.config.groups:
            return ""

        output = []
        for group, nodes in self.processor.groups():
            funcs = [node.name for node in nodes]
            funcs = '" "'.join(funcs)
            group_color = self.group_border_color.rgba_web()
            group_font_size = self.group_font_size
            output.append(
                'subgraph "cluster_{group}" {{ '
                '"{funcs}"; '
                'label = "{group}"; '
                'fontsize = "{group_font_size}"; '
                'fontcolor = "black"; '
                'style = "bold"; '
                'color="{group_color}"; }}'.format(**locals())
            )
        return output

    def generate_nodes(self):
        output = []
        for node in self.processor.nodes():
            attr = {
                "color": self.node_color_func(node).rgba_web(),
                "label": self.node_label_func(node),
            }
            output.append(self.node(node.name, attr))

        return output

    def generate_edges(self):
        output = []

        for edge in self.processor.edges():
            attr = {
                "color": self.edge_color_func(edge).rgba_web(),
                "label": self.edge_label_func(edge),
            }
            output.append(self.edge(edge, attr))

        return output
