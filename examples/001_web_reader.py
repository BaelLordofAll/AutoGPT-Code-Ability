from codex.model import Node, Parameter

request_node = Node(
    description="Takes in the url of a website",
    name="request_node",
    input_params=None,
    output_params=[
        Parameter(prama_type="str", name="url", description="The url of the website"),
        Parameter(
            prama_type="str",
            name="format",
            description="the format to convert the webpage too",
        ),
    ],
    package_requirements=[],  # Add the missing argument for "package_requirements"
)

verify_url = Node(
    description="Verifies that the url is valid",
    name="verify_url",
    input_params=[
        Parameter(prama_type="str", name="url", description="The url of the website")
    ],
    output_params=[
        Parameter(
            prama_type="str",
            name="valid_url",
            description="The url of the website if it is valid",
        )
    ],
    package_requirements=[],
)

download_page = Node(
    description="Downloads the webpage",
    name="download_page",
    input_params=[
        Parameter(
            prama_type="str",
            name="valid_url",
            description="The url of the website if it is valid",
        )
    ],
    output_params=[
        Parameter(
            prama_type="str",
            name="html",
            description="The html of the webpage",
        )
    ],
    package_requirements=[],
)

convert_page = Node(
    description="Converts the webpage to the desired format",
    name="convert_page",
    input_params=[
        Parameter(
            prama_type="str",
            name="html",
            description="The html of the webpage",
        ),
        Parameter(
            prama_type="str",
            name="format",
            description="the format to convert the webpage too",
        ),
    ],
    output_params=[
        Parameter(
            prama_type="str",
            name="converted_page",
            description="The converted webpage",
        )
    ],
    package_requirements=[],
)

response_node = Node(
    name="response_node",
    description="Returns the converted webpage",
    input_params=[
        Parameter(
            prama_type="str",
            name="converted_page",
            description="The converted webpage",
        )
    ],
    output_params=[],
    package_requirements=[],
)
