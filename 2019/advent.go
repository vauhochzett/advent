package main

import (
	"fmt"
	"strconv"
)

// --- Day 1: The Tyranny of the Rocket Equation ---

// Fuel required to launch a given module is based on its mass. Specifically, to
// find the fuel required for a module, take its mass, divide by three, round down,
// and subtract 2.

// For example:

//     For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to
//     get 2. For a mass of 14, dividing by 3 and rounding down still yields 4, so
//     the fuel required is also 2. For a mass of 1969, the fuel required is 654.
//     For a mass of 100756, the fuel required is 33583.

// The Fuel Counter-Upper needs to know the total fuel requirement. To find it,
// individually calculate the fuel needed for the mass of each module (your puzzle
// input), then add together all the fuel values.

// What is the sum of the fuel requirements for all of the modules on your
// spacecraft?

// > Total: 3391707

// --- Part Two ---

// So, for each module mass, calculate its fuel and add it to the total. Then,
// treat the fuel amount you just calculated as the input mass and repeat the
// process, continuing until a fuel requirement is zero or negative. For example:

//     A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2
//     divided by 3 and rounded down is 0, which would call for a negative fuel),
//     so the total fuel required is still just 2. At first, a module of mass 1969
//     requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216
//     then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel,
//     which requires no further fuel. So, the total fuel required for a module of
//     mass 1969 is 654 + 216 + 70 + 21 + 5 = 966. The fuel required by a module of
//     mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 +
//     12 + 2 = 50346.

// What is the sum of the fuel requirements for all of the modules on your
// spacecraft when also taking into account the mass of the added fuel? (Calculate
// the fuel requirements for each module separately, then add them all up at the
// end.)

// > Total: 5084676

func adv19Day1() {
	fmt.Println("Day 1: What is the sum of the fuel requirements for all of the modules on your spacecraft?")

	test := []int{12, 14, 1969, 100756}

	fmt.Println("Tests:")
	for _, v := range test {
		fmt.Println(v, "->", d1Fuelrequirement(v))
	}

	input := []int{78390, 73325, 52095, 126992, 106546, 81891, 69484, 131138, 95103, 53296, 115594, 79485, 130202, 95238, 99332, 136331, 124321, 127271, 108047, 69186, 90597, 96001, 138773, 55284, 127936, 110780, 89949, 85360, 55470, 110124, 101201, 139745, 148170, 149108, 79579, 139733, 52014, 125910, 77323, 145751, 52161, 105606, 132240, 69907, 144129, 116958, 60818, 144964, 111789, 85657, 115509, 84509, 50702, 69012, 110376, 134213, 127319, 92966, 58422, 144491, 128198, 84367, 94269, 147895, 105494, 88369, 117882, 146239, 50704, 62591, 149258, 63118, 145393, 122997, 136534, 96402, 121057, 59561, 86916, 75873, 68670, 147465, 62902, 145858, 137810, 108108, 97314, 118001, 54699, 56603, 66821, 80744, 124514, 143113, 132581, 79376, 105728, 115337, 111028, 52209}
	var total int = 0

	for _, v := range input {
		total += d1Fuelrequirement(v)
	}

	fmt.Println("Total:", total)
}

func d1Fuelrequirement(mass int) int {
	var fuel int = (mass / 3) - 2
	if fuel < 0 {
		return 0
	}
	return fuel + d1Fuelrequirement(fuel)
}

// --- Day 2: 1202 Program Alarm ---

// An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
// To run one, start by looking at the first integer (called position 0). Here, you
// will find an opcode - either 1, 2, or 99. The opcode indicates what to do; for
// example, 99 means that the program is finished and should immediately halt.
// Encountering an unknown opcode means something went wrong.

// Opcode 1 adds together numbers read from two positions and stores the result in
// a third position. The three integers immediately after the opcode tell you these
// three positions - the first two indicate the positions from which you should
// read the input values, and the third indicates the position at which the output
// should be stored.

// Opcode 2 works exactly like opcode 1, except it multiplies the two inputs
// instead of adding them. Again, the three integers after the opcode indicate
// where the inputs and outputs are, not their values.

// Once you're done processing an opcode, move to the next one by stepping forward
// 4 positions.

// [...]

// Here are the initial and final states of a few more small programs:

//     1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2). 2,3,0,3,99 becomes 2,3,0,6,99 (3
//     * 2 = 6). 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
//     1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.

// Once you have a working computer, the first step is to restore the gravity
// assist program (your puzzle input) to the "1202 program alarm" state it had just
// before the last computer caught fire. To do this, before running the program,
// replace position 1 with the value 12 and replace position 2 with the value 2.
// What value is left at position 0 after the program halts?

// > 0: 5110675

// --- Part Two ---

// "With terminology out of the way, we're ready to proceed. To complete the
// "gravity assist, you need to determine what pair of inputs produces the output
// "19690720."

// The inputs should still be provided to the program by replacing the values at
// addresses 1 and 2, just like before. In this program, the value placed in
// address 1 is called the noun, and the value placed in address 2 is called the
// verb. Each of the two input values will be between 0 and 99, inclusive.

// Once the program has halted, its output is available at address 0, also just
// like before. Each time you try a pair of inputs, make sure you first reset the
// computer's memory to the values in the program (your puzzle input) - in other
// words, don't reuse memory from a previous attempt.

// Find the input noun and verb that cause the program to produce the output
// 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the
// answer would be 1202.)

// 100 * noun + verb = 100 * 48 + 47 = 4847

func adv19Day2() {
	fmt.Println("Day 2: What value is left at position 0 after the program halts?")

	var tests [][]int = [][]int{
		{1, 0, 0, 3, 99},
		{1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50},
		{1, 0, 0, 0, 99},
		{2, 3, 0, 3, 99},
		{2, 4, 4, 5, 99, 0},
		{1, 1, 1, 4, 99, 5, 6, 0, 99},
	}

	fmt.Println("Tests:")

	for _, t := range tests {
		fmt.Println("   ", t)
		d2Intcode(&t)
		fmt.Println(" ->", t)
	}

	input := []int{1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 9, 1, 19, 1, 5, 19, 23, 2, 9, 23, 27, 1, 27, 5, 31, 2, 31, 13, 35, 1, 35, 9, 39, 1, 39, 10, 43, 2, 43, 9, 47, 1, 47, 5, 51, 2, 13, 51, 55, 1, 9, 55, 59, 1, 5, 59, 63, 2, 6, 63, 67, 1, 5, 67, 71, 1, 6, 71, 75, 2, 9, 75, 79, 1, 79, 13, 83, 1, 83, 13, 87, 1, 87, 5, 91, 1, 6, 91, 95, 2, 95, 13, 99, 2, 13, 99, 103, 1, 5, 103, 107, 1, 107, 10, 111, 1, 111, 13, 115, 1, 10, 115, 119, 1, 9, 119, 123, 2, 6, 123, 127, 1, 5, 127, 131, 2, 6, 131, 135, 1, 135, 2, 139, 1, 139, 9, 0, 99, 2, 14, 0, 0}

	var targetOutput int = 19690720

	var output int = 0
	var noun, verb int = 0, 0
	var minOpCode, maxOpCode int = 0, 99

	for output != targetOutput {
		// Generate new noun, verb
		verb++
		if verb > maxOpCode {
			noun++
			verb = minOpCode
		}
		if noun > maxOpCode {
			panic("Reached the end!")
		}

		program := make([]int, len(input))
		copy(program, input)

		program[1] = noun
		program[2] = verb

		d2Intcode(&program)
		if program[0] == targetOutput {
			fmt.Println("Target output achieved with noun", noun, "and verb", verb)
			fmt.Println("100 * noun + verb =", 100*noun+verb)
			break
		}
	}
}

func d2Intcode(program *[]int) {
	// Operations
	// 1 – 1 10 20 30 – ADD positions 10 and 20, store in 30
	// 2 – 2 22 23 24 – MULTIPLY (like ADD)
	// 99 – STOP
	var pos int = 0
Loop:
	for {
		var op int = (*program)[pos]
		switch op {
		case 99:
			break Loop
		case 1, 2:
			p1 := (*program)[pos+1]
			p2 := (*program)[pos+2]
			rp := (*program)[pos+3]
			d2Execute(program, op, p1, p2, rp)
			pos += 4
		default:
			panic("Invalid opcode: " + strconv.Itoa(op))
		}
	}
	return
}

func d2Execute(program *[]int, op int, p1 int, p2 int, rp int) {
	var result int = -1
	v1 := (*program)[p1]
	v2 := (*program)[p2]
	switch op {
	case 1:
		result = v1 + v2
	case 2:
		result = v1 * v2
	default:
		panic("Invalid opcode: " + string(op))
	}
	(*program)[rp] = result
}

// --- Day 3: Crossed Wires ---

// The gravity assist was successful, and you're well on your way to the Venus
// refuelling station. During the rush back on Earth, the fuel management system
// wasn't completely installed, so that's next on the priority list.

// Opening the front panel reveals a jumble of wires. Specifically, two wires are
// connected to a central port and extend outward on a grid. You trace the path
// each wire takes as it leaves the central port, one wire per line of text (your
// puzzle input).

// The wires twist and turn, but the two wires occasionally cross paths. To fix the
// circuit, you need to find the intersection point closest to the central port.
// Because the wires are on a grid, use the Manhattan distance for this
// measurement. While the wires do technically cross right at the central port
// where they both start, this point does not count, nor does a wire count as
// crossing with itself.

// What is the Manhattan distance from the central port to the closest
// intersection?

func adv19Day3() {
	fmt.Println("Day 3: What is the Manhattan distance from the central port to",
		"the closest intersection?")

	test := [][]string{
		{"R8", "U5", "L5", "D3"},
		{"U7", "R6", "D4", "L4"},
	}

	if test[0][0] != "" {
		// PASS
	}

	// fmt.Println("Test: Expecting 6")
	// fmt.Println("Result:", wireIntersectionDistance(test))

	input := [][]string{
		{"R991", "U557", "R554", "U998", "L861", "D301", "L891", "U180", "L280", "D103", "R828", "D58", "R373", "D278", "L352", "D583", "L465", "D301", "R384", "D638", "L648", "D413", "L511", "U596", "L701", "U463", "L664", "U905", "L374", "D372", "L269", "U868", "R494", "U294", "R661", "U604", "L629", "U763", "R771", "U96", "R222", "U227", "L97", "D793", "L924", "U781", "L295", "D427", "R205", "D387", "L455", "D904", "R254", "D34", "R341", "U268", "L344", "D656", "L715", "U439", "R158", "U237", "R199", "U729", "L428", "D125", "R487", "D506", "R486", "D496", "R932", "D918", "R603", "U836", "R258", "U15", "L120", "U528", "L102", "D42", "R385", "U905", "L472", "D351", "R506", "U860", "L331", "D415", "R963", "D733", "R108", "D527", "L634", "U502", "L553", "D623", "R973", "U209", "L632", "D588", "R264", "U553", "L768", "D689", "L708", "D432", "R247", "U993", "L146", "U656", "R710", "U47", "R783", "U643", "R954", "U888", "L84", "U202", "R495", "U66", "R414", "U993", "R100", "D557", "L326", "D645", "R975", "U266", "R143", "U730", "L491", "D96", "L161", "U165", "R97", "D379", "R930", "D613", "R178", "D635", "R192", "U957", "L450", "U149", "R911", "U220", "L914", "U659", "L67", "D825", "L904", "U137", "L392", "U333", "L317", "U310", "R298", "D240", "R646", "U588", "R746", "U861", "L958", "D892", "L200", "U463", "R246", "D870", "R687", "U815", "R969", "U864", "L972", "U254", "L120", "D418", "L567", "D128", "R934", "D217", "R764", "U128", "R146", "U467", "R690", "U166", "R996", "D603", "R144", "D362", "R885", "D118", "L882", "U612", "R270", "U917", "L599", "D66", "L749", "D498", "L346", "D920", "L222", "U439", "R822", "U891", "R458", "U15", "R831", "U92", "L164", "D615", "L439", "U178", "R409", "D463", "L452", "U633", "L683", "U186", "R402", "D609", "L38", "D699", "L679", "D74", "R125", "D145", "R424", "U961", "L353", "U43", "R794", "D519", "L359", "D494", "R812", "D770", "L657", "U154", "L137", "U549", "L193", "D816", "R333", "U650", "R49", "D459", "R414", "U72", "R313", "U231", "R370", "U680", "L27", "D221", "L355", "U342", "L597", "U748", "R821", "D280", "L307", "U505", "L160", "U982", "L527", "D516", "L245", "U158", "R565", "D797", "R99", "D695", "L712", "U155", "L23", "U964", "L266", "U623", "L317", "U445", "R689", "U150", "L41", "U536", "R638", "D200", "R763", "D260", "L234", "U217", "L881", "D576", "L223", "U39", "L808", "D125", "R950", "U341", "L405"},
		{"L993", "D508", "R356", "U210", "R42", "D68", "R827", "D513", "L564", "D407", "L945", "U757", "L517", "D253", "R614", "U824", "R174", "D536", "R906", "D291", "R70", "D295", "R916", "D754", "L892", "D736", "L528", "D399", "R76", "D588", "R12", "U617", "R173", "D625", "L533", "D355", "R178", "D706", "R139", "D419", "R460", "U976", "L781", "U973", "L931", "D254", "R195", "U42", "R555", "D151", "R226", "U713", "L755", "U398", "L933", "U264", "R352", "U461", "L472", "D810", "L257", "U901", "R429", "U848", "L181", "D362", "R404", "D234", "L985", "D392", "R341", "U608", "L518", "D59", "L804", "D219", "L366", "D28", "L238", "D491", "R265", "U131", "L727", "D504", "R122", "U461", "R732", "D411", "L910", "D884", "R954", "U341", "L619", "D949", "L570", "D823", "R646", "D226", "R197", "U892", "L691", "D294", "L955", "D303", "R490", "D469", "L503", "D482", "R390", "D741", "L715", "D187", "R378", "U853", "L70", "D903", "L589", "D481", "L589", "U911", "R45", "U348", "R214", "D10", "R737", "D305", "R458", "D291", "R637", "D721", "R440", "U573", "R442", "D407", "L63", "U569", "L903", "D936", "R518", "U859", "L370", "D888", "R498", "D759", "R283", "U469", "R548", "D185", "R808", "D81", "L629", "D761", "R807", "D878", "R712", "D183", "R382", "D484", "L791", "D371", "L188", "D397", "R645", "U679", "R415", "D446", "L695", "U174", "R707", "D36", "R483", "U877", "L819", "D538", "L277", "D2", "R200", "D838", "R837", "U347", "L865", "D945", "R958", "U575", "L924", "D351", "L881", "U961", "R899", "U845", "R816", "U866", "R203", "D380", "R766", "D97", "R38", "U148", "L999", "D332", "R543", "U10", "R351", "U281", "L460", "U309", "L543", "U795", "L639", "D556", "L882", "D513", "R722", "U314", "R531", "D604", "L418", "U840", "R864", "D694", "L530", "U862", "R559", "D639", "R689", "D201", "L439", "D697", "R441", "U175", "R558", "D585", "R92", "D191", "L533", "D788", "R154", "D528", "R341", "D908", "R811", "U750", "R172", "D742", "R113", "U56", "L517", "D826", "L250", "D269", "L278", "U74", "R285", "U904", "L221", "U270", "R296", "U671", "L535", "U340", "L206", "U603", "L852", "D60", "R648", "D313", "L282", "D685", "R482", "U10", "R829", "U14", "L12", "U365", "R996", "D10", "R104", "U654", "R346", "D458", "R219", "U247", "L841", "D731", "R115", "U400", "L731", "D904", "L487", "U430", "R612", "U437", "L865", "D618", "R747", "U522", "R309", "U302", "R9", "U609", "L201"},
	}
	// First:  x: [-3468, 6388] | y: [  -940, 9397]
	// Second: x: [-7512, 2129] | y: [-13610,   42]
	// Total:  x: [-7512, 6388] | y: [-13610, 9397]
	// 0-corrected (top-left is 0,0), padded: x: [0, 13902] | y: [0, 23009]
	// Start point for squared, 0-corrected, padded field: x 7513 | y 13611
	//    (reasoning: max negative must be == 1; 7513 - 7512 = 1)
	sizeX, sizeY := measureField(input)
	fmt.Println("sizeX:", sizeX, "sizeY:", sizeY)

	wireIntersectionDistance(input, sizeX, sizeY)
}

func wireIntersectionDistance(wires [][]string, sizeX int, sizeY int) (distance int) {
	// TODO IMPLEMENT
	panic("Not implemented!")
}

// measureField measures the dimensions of the field given by the direction commands passed in.
// sizeX is the width (so the size from left to right)
// sizeY is the height (from top to bottom)
func measureField(commandLists [][]string) (sizeX int, sizeY int) {
	maxX, maxY, minX, minY := 0, 0, 0, 0
	for _, commands := range commandLists {
		x, y := 0, 0
		for _, p := range commands {
			d, l := parsePath(p)
			switch d {
			case "R":
				x += l
			case "L":
				x -= l
			case "U":
				y += l
			case "D":
				y -= l
			}

			if x > maxX {
				maxX = x
			} else if x < minX {
				minX = x
			}
			if y > maxY {
				maxY = y
			} else if y < minY {
				minY = y
			}
		}
	}
	if maxX < 0 || maxY < 0 || minX > 0 || minY > 0 {
		panic("Unexpected value!")
	}
	sizeX = maxX - minX
	sizeY = maxY - minY
	return
}

func parsePath(path string) (direction string, length int) {
	pathRunes := []rune(path)
	direction = string(pathRunes[0])
	length, err := strconv.Atoi(string(pathRunes[1:]))
	if err != nil {
		panic(err.Error())
	}
	return
}

func main() {
	fmt.Println("Advent of Code 2019")
	adv19Day3()
}
