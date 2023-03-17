# Copyright (c) Meta Platforms, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

add_library(llvm_lex LLLexer.cc llvm_lexer_token_info.cc)

target_include_directories(llvm_lex PUBLIC ${LLVM_INCLUDE_DIRS})
llvm_map_components_to_libnames(llvm_libs core support bitwriter)
target_link_libraries(llvm_lex ${llvm_libs})
