get_filename_component(app_proto "app.proto" ABSOLUTE)
get_filename_component(app_proto_path "${app_proto}" PATH)

set(app_proto_srcs "${generated_header_dir}/miniapp/app.pb.cc")
set(app_proto_hdrs "${generated_header_dir}/miniapp/app.pb.h")
set(app_grpc_srcs "${generated_header_dir}/miniapp/app.grpc.pb.cc")
set(app_grpc_hdrs "${generated_header_dir}/miniapp/app.grpc.pb.h")

add_custom_command(
    OUTPUT
        "${app_proto_srcs}"
        "${app_proto_hdrs}"
        "${app_grpc_srcs}"
        "${app_grpc_hdrs}"
    COMMAND ${PROTOC}
    ARGS
        --grpc_out
        "${generated_header_dir}/miniapp"
        --cpp_out
        "${generated_header_dir}/miniapp"
        -I
        "${app_proto_path}"
        --plugin=protoc-gen-grpc="${GRPC_CPP_PLUGIN}"
        "${app_proto}"
    DEPENDS "${app_proto}"
)

# add_library(
#     app_proto
#     ${app_grpc_srcs}
#     ${app_grpc_hdrs}
#     ${app_proto_srcs}
#     ${app_proto_hdrs}
# )
# target_link_libraries(
#     app_proto
#     PRIVATE
#     protobuf::libprotobuf
#     gRPC::grpc++
#     gRPC::grpc++_reflection
# )

add_executable(
    app
    main.cc
    ${app_grpc_srcs}
    ${app_grpc_hdrs}
    ${app_proto_srcs}
    ${app_proto_hdrs}
)
target_compile_options(
    app
    PRIVATE
        # NOTE(cummins): Workaround for libprotobuf bug.
        -DNDEBUG
)
target_link_libraries(
    app
    PRIVATE ${PROTOBUF_LDFLAGS}
    # gRPC::grpc++
    # gRPC::grpc++_reflection
)
