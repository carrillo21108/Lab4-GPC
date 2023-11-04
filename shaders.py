#En OpenGL, los shaders se escriben enn un
#nuevo lenguaje de programacion llamada GLSL
#Graphics Library Shader Language

vertex_shader = '''
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 pos = position;
    pos.y += sin(time+pos.x/2+pos.z)/2;
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(pos,1.0);
    UVs = texCoords;
    outNormals = (modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
}
'''

fat_vertex_shader = '''
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float fatness;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    outNormals  =(modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position+(fatness/4)*outNormals;
    
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(pos,1.0);
    UVs = texCoords;
}
'''

fragment_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    fragColor = texture(tex,UVs)*intensity;
}

'''

toon_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    if (intensity<0.33)
        intensity=0.2;
    else if (intensity<0.66)
        intensity=0.6;
    else
        intensity=1.0;
    fragColor = texture(tex,UVs)*intensity;
}

'''

gourad_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    fragColor = texture(tex,UVs)*intensity;
}

'''

unlit_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex,UVs);
}

'''

siren_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform float time;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    
    vec3 dir1 = vec3(sin(time),0,cos(time)); 
    vec3 dir2 = vec3(cos(time),0,sin(time));
    vec3 dir3 = vec3(0,sin(time),cos(time));
    
    float diffuse1 = pow(dot(outNormals,dir1),2.0);
    float diffuse2 = pow(dot(outNormals,dir2),2.0);
    float diffuse3 = pow(dot(outNormals,dir3),2.0);
    
    vec3 col1 = diffuse1 * vec3(1,0,0);
    vec3 col2 = diffuse2 * vec3(0,0,1);
    vec3 col3 = diffuse3 * vec3(0,1,0);
    
    fragColor = vec4(col1 + col2 + col3, 1.0);
}

'''