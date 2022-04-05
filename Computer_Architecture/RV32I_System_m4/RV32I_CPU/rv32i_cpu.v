//
//  Author: Prof. Taeweon Suh
//          Computer Science & Engineering
//          Korea University
//  Date: July 14, 2020
//  Description: Skeleton design of RV32I Single-cycle CPU
//

`timescale 1ns/1ns
`define simdelay 1

module rv32i_cpu (
		      input         clk, reset,
            output [31:0] pc,		  		// program counter for instruction fetch
            input  [31:0] inst, 			// incoming instruction
            output        Memwrite, 	// 'memory write' control signal
            output [31:0] Memaddr,  	// memory address 
            output [31:0] MemWdata, 	// data to write to memory
            input  [31:0] MemRdata); 	// data read from memory

  wire        auipc, lui;
  wire        alusrc, regwrite;
  wire [4:0]  alucontrol;
  wire        memtoreg, memwrite;
  wire        branch, jal, jalr;
  wire 		  stall;
  
  // ###### JaeWon Choi: Start######
  reg [31:0] inst_ifid;
  reg [4:0]alucontrol_idex;
  reg auipc_idex, lui_idex;
  reg memtoreg_idex, memwrite_idex, branch_idex, alusrc_idex;
  reg regwrite_idex, jal_idex, jalr_idex;
  reg memwrite_exmem;
  
  
  always @(posedge clk)
  begin
  if (stall)
  begin 
	  inst_ifid <= #`simdelay inst_ifid;
	  auipc_idex <= #`simdelay 1'b0;
	  lui_idex <= #`simdelay 1'b0;
	  memtoreg_idex <= #`simdelay 1'b0;
	  memwrite_idex <= #`simdelay 1'b0;
	  branch_idex  <= #`simdelay 1'b0;
	  alusrc_idex <= #`simdelay 1'b0;
	  regwrite_idex <= #`simdelay 1'b0;
	  jal_idex <= #`simdelay 1'b0;
	  jalr_idex <= #`simdelay 1'b0;
	  alucontrol_idex <= #`simdelay 5'b00000;
  end
  else
  begin
  	  inst_ifid <= #`simdelay inst;
	  
	  auipc_idex <= #`simdelay auipc;
	  lui_idex <= #`simdelay lui;
	  memtoreg_idex <= #`simdelay memtoreg;
	  memwrite_idex <= #`simdelay memwrite;
	  branch_idex  <= #`simdelay branch;
	  alusrc_idex <= #`simdelay alusrc;
	  regwrite_idex <= #`simdelay regwrite;
	  jal_idex <= #`simdelay jal;
	  jalr_idex <= #`simdelay jalr;
	  alucontrol_idex <= #`simdelay alucontrol;
  end
  
	  memwrite_exmem <= #`simdelay memwrite_idex;
	  
  end
  
  assign Memwrite = memwrite_exmem;
  
// ###### JaeWon Choi: End ######
 
	
  // Instantiate Controller
  controller i_controller(
      .opcode		(inst_ifid[6:0]), 
		.funct7		(inst_ifid[31:25]), 
		.funct3		(inst_ifid[14:12]), 
		.auipc		(auipc),
		.lui			(lui),
		.memtoreg	(memtoreg),
		.memwrite	(memwrite),
		.branch		(branch),
		.alusrc		(alusrc),
		.regwrite	(regwrite),
		.jal			(jal),
		.jalr			(jalr),
		.alucontrol	(alucontrol));

  // Instantiate Datapath
  datapath i_datapath(
		.clk				(clk),
		.reset			(reset),
		.auipc			(auipc_idex),
		.lui				(lui_idex),
		.memtoreg		(memtoreg_idex),
		.memwrite		(memwrite_idex),
		.branch			(branch_idex),
		.alusrc			(alusrc_idex),
		.regwrite		(regwrite_idex),
		.jal				(jal_idex),
		.jalr				(jalr_idex),
		.alucontrol		(alucontrol_idex),
		.pc				(pc),
		.inst				(inst_ifid),
		.aluout			(Memaddr), 
		.MemWdata		(MemWdata),
		.MemRdata		(MemRdata),
		.stall         (stall));

endmodule


//
// Instruction Decoder 
// to generate control signals for datapath
//
module controller(input  [6:0] opcode,
                  input  [6:0] funct7,
                  input  [2:0] funct3,
                  output       auipc,
                  output       lui,
                  output       alusrc,
                  output [4:0] alucontrol,
                  output       branch,
                  output       jal,
                  output       jalr,
                  output       memtoreg,
                  output       memwrite,
                  output       regwrite);

	maindec i_maindec(
		.opcode		(opcode),
		.auipc		(auipc),
		.lui			(lui),
		.memtoreg	(memtoreg),
		.memwrite	(memwrite),
		.branch		(branch),
		.alusrc		(alusrc),
		.regwrite	(regwrite),
		.jal			(jal),
		.jalr			(jalr));

	aludec i_aludec( 
		.opcode     (opcode),
		.funct7     (funct7),
		.funct3     (funct3),
		.alucontrol (alucontrol));


endmodule


//
// RV32I Opcode map = Inst[6:0]
//
`define OP_R			7'b0110011
`define OP_I_Arith	7'b0010011
`define OP_I_Load  	7'b0000011
`define OP_I_JALR  	7'b1100111
`define OP_S			7'b0100011
`define OP_B			7'b1100011
`define OP_U_LUI		7'b0110111
`define OP_J_JAL		7'b1101111
//
// Main decoder generates all control signals except alucontrol 
//
//
module maindec(input  [6:0] opcode,
               output       auipc,
               output       lui,
               output       regwrite,
               output       alusrc,
               output       memtoreg, memwrite,
               output       branch, 
               output       jal,
               output       jalr);

  reg [8:0] controls;

  assign {auipc, lui, regwrite, alusrc, 
			 memtoreg, memwrite, branch, jal, 
			 jalr} = controls;

  always @(*)
  begin
    case(opcode)
      `OP_R: 			controls <= #`simdelay 9'b0010_0000_0; // R-type
      `OP_I_Arith: 	controls <= #`simdelay 9'b0011_0000_0; // I-type Arithmetic
      `OP_I_Load: 	controls <= #`simdelay 9'b0011_1000_0; // I-type Load
      `OP_S: 			controls <= #`simdelay 9'b0001_0100_0; // S-type Store
      `OP_B: 			controls <= #`simdelay 9'b0000_0010_0; // B-type Branch
      `OP_U_LUI: 		controls <= #`simdelay 9'b0111_0000_0; // LUI
      `OP_J_JAL: 		controls <= #`simdelay 9'b0011_0001_0; // JAL
		`OP_I_JALR: 	controls <= #`simdelay 9'b0011_0000_1; // JALR (j1)
      default:    	controls <= #`simdelay 9'b0000_0000_0; // ???
    endcase
  end

endmodule

//
// ALU decoder generates ALU control signal (alucontrol)
//
module aludec(input      [6:0] opcode,
              input      [6:0] funct7,
              input      [2:0] funct3,
              output reg [4:0] alucontrol);

  always @(*)

    case(opcode)

      `OP_R:   		// R-type
		begin
			case({funct7,funct3})
			 10'b0000000_000: alucontrol <= #`simdelay 5'b00000; // addition (add)
			 10'b0100000_000: alucontrol <= #`simdelay 5'b10000; // subtraction (sub)
			 10'b0000000_111: alucontrol <= #`simdelay 5'b00001; // and (and)
			 10'b0000000_110: alucontrol <= #`simdelay 5'b00010; // or (or)
          default:         alucontrol <= #`simdelay 5'bxxxxx; // ???
        endcase
		end

      `OP_I_Arith:   // I-type Arithmetic
		begin
			case(funct3)
			 3'b000:  alucontrol <= #`simdelay 5'b00000; // addition (addi)
			 3'b110:  alucontrol <= #`simdelay 5'b00010; // or (ori)
			 3'b111:  alucontrol <= #`simdelay 5'b00001; // and (andi)
			 3'b100:  alucontrol <= #`simdelay 5'b00011; // xori (xori) (j1)
			 3'b001:  alucontrol <= #`simdelay 5'b00100; // slli (slli) (j1)
          default: alucontrol <= #`simdelay 5'bxxxxx; // ???
        endcase
		end

      `OP_I_Load: 	// I-type Load (LW, LH, LB...)
      	alucontrol <= #`simdelay 5'b00000;  // addition 

      `OP_B:   		// B-type Branch (BEQ, BNE, ..
      	alucontrol <= #`simdelay 5'b10000; //subtraction
			
      `OP_S:   		// S-type Store (SW, SH, SB)
      	alucontrol <= #`simdelay 5'b00000;  // addition 

      `OP_U_LUI: 		// U-type (LUI)
      	alucontrol <= #`simdelay 5'b00000;  // addition

      default: 
      	alucontrol <= #`simdelay 5'b00000;  // 

    endcase
    
endmodule


//
// CPU datapath
//
module datapath(input         clk, reset,
                input  [31:0] inst,
                input         auipc,
                input         lui,
                input         regwrite,
                input         memtoreg,
                input         memwrite,
                input         alusrc, 
                input  [4:0]  alucontrol,
                input         branch,
                input         jal,
                input         jalr,

                output reg [31:0] pc,
					 output reg stall,
					 output [31:0] aluout,
                output [31:0] MemWdata,
                input  [31:0] MemRdata);

  wire [4:0]  rs1, rs2, rd;
  wire [2:0]  funct3;
  wire [31:0] rs1_data, rs2_data;
  reg  [31:0] rd_data;
  wire [20:1] jal_imm;
  wire [31:0] se_jal_imm;
  wire [12:1] jalr_imm;
  wire [31:0] se_jalr_imm; 
  wire [12:1] br_imm;
  wire [31:0] se_br_imm;
  wire [31:0] se_imm_itype;
  wire [31:0] se_imm_stype;
  wire [31:0] auipc_lui_imm;
  reg  [31:0] alusrc1;
  reg  [31:0] alusrc2;
  wire [31:0] branch_dest, jal_dest, jalr_dest;
  wire		  Nflag, Zflag, Cflag, Vflag;
  wire		  f3beq, f3blt, f3bgeu; //(j1)
  wire		  beq_taken;
  wire		  bgeu_taken; //(j1)
  wire		  blt_taken;
  
  assign rs1 = inst[19:15];
  assign rs2 = inst[24:20];
  assign rd  = inst[11:7]; 
  assign funct3  = inst[14:12];

 // ##### JaeWon Choi: Start #######
  reg [31:0] pc_ifid;
  //------------------------------------------------------------------------------
  reg [31:0] pc_idex;
  reg [4:0]  rs1_idex, rs2_idex;
  reg [4:0]  rd_idex;
  reg [31:0] rs1_data_idex, rs2_data_idex;
  reg [31:0] se_jal_imm_idex, se_jalr_imm_idex, se_br_imm_idex, se_imm_itype_idex, se_imm_stype_idex, auipc_lui_imm_idex;
  //----------------------------------------------------------------------------------------------------------------------
  reg [31:0] pc_exmem; // pc needs to be passed on at each stage 
  reg [31:0] rs2_data_exmem;// exmem has rs2 also 
  reg [4:0]  rd_exmem;
  reg [31:0] aluout_exmem;
  reg branch_exmem, Nflag_exmem, Vflag_exmem, Cflag_exmem, Zflag_exmem, memwrite_exmem, memtoreg_exmem, jal_exmem, jalr_exmem, regwrite_exmem;
  reg [31:0] branch_dest_exmem, jalr_dest_exmem, jal_dest_exmem;
  reg [2:0]  funct3_exmem;
  //-----------------------------------------------------------------------------------------------------------------------------------------
  reg [4:0]  rd_memwb;
  reg regwrite_memwb, memtoreg_memwb;
  reg [31:0] aluout_memwb, MemRdata_memwb;
  wire[31:0] aluout_2;
  //####### JaeWon Choi: End ######

  //
  // PC (Program Counter) logic 
  //
  assign f3beq  = (funct3_exmem == 3'b000);
  assign f3blt  = (funct3_exmem == 3'b100);
  assign f3bgeu  = (funct3_exmem == 3'b111); // bgeu(j1) 

  assign beq_taken  =  branch_exmem & f3beq & Zflag_exmem;
  assign blt_taken  =  branch_exmem & f3blt & (Nflag_exmem != Vflag_exmem);
  assign bgeu_taken =  branch_exmem & f3bgeu & Cflag_exmem; //bgeu

  assign branch_dest = (pc_idex + se_br_imm_idex);
  assign jal_dest 	= (pc_idex + se_jal_imm_idex);
  assign jalr_dest   = (aluout_2); //new
  
  always @(posedge clk)
  begin
      // ###### JaeWon Choi: Start ######
	  pc_ifid <= #`simdelay pc; 
//-----------------------	----------------------------------------------	  
	  pc_idex <= #`simdelay pc_ifid; 
	  rs1_idex <= #`simdelay rs1;
	  rs2_idex <= #`simdelay rs2;
	  
	  begin // when previous results need to be used
		  if ((rd_memwb == rs1) & regwrite_memwb & (rd_memwb !=0 ))
				 rs1_data_idex <= #`simdelay rd_data;
		  else rs1_data_idex <= #`simdelay rs1_data;
	  end
	  begin
		  if ((rd_memwb == rs2) & regwrite_memwb & (rd_memwb !=0 ))
				 rs2_data_idex <= #`simdelay rd_data;
		  else rs2_data_idex <= #`simdelay rs2_data;
	  end
	  
	  rd_idex <= #`simdelay rd;
	  se_jal_imm_idex <= #`simdelay se_jal_imm;
	  se_jalr_imm_idex <= #`simdelay se_jalr_imm;
	  se_br_imm_idex <= #`simdelay se_br_imm;
	  se_imm_itype_idex <= #`simdelay se_imm_itype;
	  se_imm_stype_idex <= #`simdelay se_imm_stype;
	  auipc_lui_imm_idex <= #`simdelay auipc_lui_imm;
//-----------------------------------------------------------------------------------	  
	  pc_exmem <= #`simdelay pc_idex;
	  rd_exmem <= #`simdelay rd_idex;	  
	  branch_exmem <= #`simdelay branch;
	  funct3_exmem <= #`simdelay funct3;
	  memtoreg_exmem <= #`simdelay memtoreg;
	  regwrite_exmem <= #`simdelay regwrite;
	  memwrite_exmem <= #`simdelay memwrite;
	  Nflag_exmem <= #`simdelay Nflag;
	  Vflag_exmem <= #`simdelay Vflag;
	  Cflag_exmem <= #`simdelay Cflag;
	  Zflag_exmem  <= #`simdelay Zflag;
	  jal_exmem <= #`simdelay jal;
	  jalr_exmem <= #`simdelay jalr;
	  jalr_dest_exmem <= #`simdelay jalr_dest;
	  jal_dest_exmem <= #`simdelay jal_dest;
	  branch_dest_exmem <= #`simdelay branch_dest;
	  aluout_exmem <= #`simdelay aluout_2;
	  
	  begin
		  if((rd_exmem == rs2_idex) & (memwrite == 1)) 
				rs2_data_exmem <= #`simdelay aluout_exmem;
		  else if((rd_memwb == rs2_idex) & (memwrite == 1)) 
				rs2_data_exmem <= #`simdelay rd_data;
	     else rs2_data_exmem <= #`simdelay rs2_data_idex;
	  end 
//------------------------------------------------------------------------------------	  
	  rd_memwb <= #`simdelay rd_exmem;
	  aluout_memwb <= #`simdelay aluout_exmem;
	  MemRdata_memwb <= #`simdelay MemRdata;
	  regwrite_memwb  <= #`simdelay regwrite_exmem;
	  memtoreg_memwb  <= #`simdelay memtoreg_exmem;
	  
	  
	end	
	
	always@(*)
	begin
		if((memtoreg == 1) & ((rd_idex == rs1) | (rd_idex == rs2))) //make bubbles cuz after memory access we can use
				stall = 1;
		else  stall = 0;
	end
	//###### JaeWon Choi: End ######	
	always @(posedge clk, posedge reset)
	begin
     if (reset)  pc <= 32'b0;
	  else 
	  begin
			if (stall)
				pc <= #`simdelay pc;
	      else if (beq_taken | blt_taken | bgeu_taken)
				pc <= #`simdelay branch_dest_exmem;
		   else if (jal) 
				pc <= #`simdelay jal_dest_exmem;
		   else if (jalr)
				pc <= #`simdelay jalr_dest_exmem;
			
			else
				pc <= #`simdelay (pc + 4);
	  end
  end

  assign aluout = aluout_exmem;
  
  
  // JAL immediate
  assign jal_imm[20:1] = {inst[31],inst[19:12],inst[20],inst[30:21]};
  assign se_jal_imm[31:0] = {{11{jal_imm[20]}},jal_imm[20:1],1'b0};
  
  // Branch immediate
  assign br_imm[12:1] = {inst[31],inst[7],inst[30:25],inst[11:8]};
  assign se_br_imm[31:0] = {{19{br_imm[12]}},br_imm[12:1],1'b0};


  // 
  // Register File 
  //
  regfile i_regfile(
    .clk			(clk),
    .we			(regwrite_memwb),
    .rs1			(rs1),
    .rs2			(rs2),
    .rd			(rd_memwb),
    .rd_data	(rd_data),
    .rs1_data	(rs1_data),
    .rs2_data	(rs2_data));


	assign MemWdata = rs2_data_exmem;


	//
	// ALU 
	//
	alu i_alu(
		.a			(alusrc1),
		.b			(alusrc2),
		.alucont	(alucontrol),
		.result	(aluout_2),
		.N			(Nflag),
		.Z			(Zflag),
		.C			(Cflag),
		.V			(Vflag));

	// 1st source to ALU (alusrc1)
	//###### JaeWon Choi: Start ######
	always@(*)
	begin
		if ((rd_exmem == rs1_idex) & regwrite_exmem & (rd_exmem != 0)) alusrc1 = aluout_exmem; //gets the rs1 after the excution of the previous stage
		else if ((rd_memwb == rs1_idex) & regwrite_memwb & (rd_memwb !=0)) alusrc1 = rd_data;
		else if (auipc)	alusrc1[31:0]  =  pc_idex;
		else if (lui) 		alusrc1[31:0]  =  32'b0;
		else          		alusrc1[31:0]  =  rs1_data_idex[31:0];
	end
	
	// 2nd source to ALU (alusrc2)
	always@(*)
	begin
		if ((rd_exmem == rs2_idex) & regwrite_exmem & (rd_exmem != 0) & (alusrc != 1)) alusrc2 = aluout_exmem;
		else if ((rd_memwb == rs2_idex) & regwrite_memwb & (rd_memwb !=0) & (alusrc != 1)) alusrc2 = rd_data;
		else if (auipc | lui)			alusrc2[31:0] = auipc_lui_imm_idex[31:0]; 
		else if (alusrc & memwrite)	alusrc2[31:0] = se_imm_stype_idex[31:0]; 
		else if (alusrc)					alusrc2[31:0] = se_imm_itype_idex[31:0]; 
		else									alusrc2[31:0] = rs2_data_idex[31:0]; 
	end
	
	assign se_imm_itype[31:0] = {{20{inst[31]}},inst[31:20]};
	assign se_imm_stype[31:0] = {{20{inst[31]}},inst[31:25],inst[11:7]};
	assign auipc_lui_imm[31:0] = {inst[31:12],12'b0};
	//###### JaeWon Choi: End ######


	// Data selection for writing to RF
	always@(*)
	begin
		if	     (jal_exmem | jalr_exmem)			rd_data[31:0] = pc_exmem + 4;
		else if (memtoreg_memwb)	rd_data[31:0] = MemRdata_memwb; 
		else								rd_data[31:0] = aluout_memwb; 
	end
	
endmodule
