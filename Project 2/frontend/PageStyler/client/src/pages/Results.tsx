import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import ScheduleVisualizer from "@/components/ScheduleVisualizer";
import { useAppStore } from "@/lib/store";

// Helper function to convert days string to array
function parseDaysToArray(days: string): string[] {
  if (!days || days.trim() === '') {
    console.warn('Empty days string received');
    return [];
  }

  const dayMap: Record<string, string> = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'R': 'Thursday',
    'F': 'Friday'
  };

  const result = days.split('').map(d => dayMap[d] || d).filter(d => d !== ' ');

  if (result.some(d => !['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].includes(d))) {
    console.warn(`Invalid days parsed from "${days}":`, result);
  }

  return result;
}

// Helper function to format time
function formatTime(timeString: string): string {
  // Convert "09:30 AM" or "09:30:00 AM" or "12:00 PM" to 24-hour "09:30" or "12:00"
  const match = timeString.match(/(\d{1,2}):(\d{2})(?::\d{2})?\s*(AM|PM)/i);
  if (!match) {
    // If no AM/PM found, just extract HH:MM
    const simpleMatch = timeString.match(/(\d{1,2}:\d{2})/);
    return simpleMatch ? simpleMatch[1] : timeString;
  }

  let hours = parseInt(match[1]);
  const minutes = match[2];
  const period = match[3].toUpperCase();

  // Convert to 24-hour format
  if (period === 'PM' && hours !== 12) {
    hours += 12;
  } else if (period === 'AM' && hours === 12) {
    hours = 0;
  }

  // Format as HH:MM
  return `${hours.toString().padStart(2, '0')}:${minutes}`;
}

// Mock data for demonstration (kept for fallback)
const MOCK_SCHEDULES = [
  {
    id: "A",
    matchPercentage: 98,
    creditHours: 15,
    courses: [
      {
        title: "CS 124: Intro to Computer Science I",
        description: "Basic concepts in computing and fundamental techniques for solving computational problems.",
        weekdays: ["Monday", "Wednesday", "Friday"],
        time: "09:00-09:50",
        courseData: {
          course: "CS 124",
          name: "Introduction to Computer Science I",
          description: "Full description...",
          credit: "3 hours",
          degree: "Quant I",
          CRN: 71578,
          section: "AL1",
          term: "1",
          type: "Lecture",
          start: "09:00:00 am",
          end: "09:50:00 am",
          days: "MWF",
          building: "Siebel Center",
          room: "1404",
          location: "Siebel Center 1404",
          instructors: "Challen, G"
        }
      },
      {
        title: "MATH 221: Calculus I",
        description: "First course in calculus and analytic geometry.",
        weekdays: ["Tuesday", "Thursday"],
        time: "11:00-12:20",
        courseData: {
          course: "MATH 221",
          name: "Calculus I",
          description: "Calc I...",
          credit: "4 hours",
          degree: "Quant I",
          CRN: 34123,
          section: "BL2",
          term: "1",
          type: "Lecture",
          start: "11:00:00 am",
          end: "12:20:00 pm",
          days: "TR",
          building: "Altgeld Hall",
          room: "314",
          location: "Altgeld Hall 314",
          instructors: "Smith, A"
        }
      },
      {
        title: "PHYS 211: University Physics: Mechanics",
        description: "Newton's Laws, work and energy, static properties of fluids, oscillations, transverse waves, systems of particles.",
        weekdays: ["Monday", "Wednesday"],
        time: "13:00-14:50",
        courseData: {
          course: "PHYS 211",
          name: "University Physics: Mechanics",
          description: "Physics...",
          credit: "4 hours",
          degree: "Physical Sciences",
          CRN: 56789,
          section: "C3",
          term: "1",
          type: "Lab",
          start: "01:00:00 pm",
          end: "02:50:00 pm",
          days: "MW",
          building: "Loomis Lab",
          room: "141",
          location: "Loomis Lab 141",
          instructors: "Doe, J"
        }
      },
      {
        title: "ECON 102: Microeconomic Principles",
        description: "Introduction to the functions of individual decision-makers, both consumers and producers, within the larger economic system.",
        weekdays: ["Monday", "Wednesday", "Friday"],
        time: "15:00-15:50",
        courseData: {
          course: "ECON 102",
          name: "Microeconomic Principles",
          description: "Micro...",
          credit: "3 hours",
          degree: "Social Sciences",
          CRN: 90123,
          section: "D4",
          term: "1",
          type: "Lecture",
          start: "03:00:00 pm",
          end: "03:50:00 pm",
          days: "MWF",
          building: "David Kinley Hall",
          room: "114",
          location: "David Kinley Hall 114",
          instructors: "Vasquez, M"
        }
      }
    ]
  },
  {
    id: "B",
    matchPercentage: 94,
    creditHours: 16,
    courses: [
      {
        title: "CS 124: Intro to Computer Science I",
        description: "Basic concepts in computing and fundamental techniques for solving computational problems.",
        weekdays: ["Tuesday", "Thursday"],
        time: "09:30-10:45",
        courseData: {
          course: "CS 124",
          name: "Introduction to Computer Science I",
          description: "Full description...",
          credit: "3 hours",
          degree: "Quant I",
          CRN: 71579,
          section: "AL2",
          term: "1",
          type: "Lecture",
          start: "09:30:00 am",
          end: "10:45:00 am",
          days: "TR",
          building: "Siebel Center",
          room: "1404",
          location: "Siebel Center 1404",
          instructors: "Challen, G"
        }
      },
      {
        title: "MATH 221: Calculus I",
        description: "First course in calculus and analytic geometry.",
        weekdays: ["Monday", "Wednesday", "Friday"],
        time: "10:00-10:50",
        courseData: {
          course: "MATH 221",
          name: "Calculus I",
          description: "Calc I...",
          credit: "4 hours",
          degree: "Quant I",
          CRN: 34124,
          section: "BL3",
          term: "1",
          type: "Lecture",
          start: "10:00:00 am",
          end: "10:50:00 am",
          days: "MWF",
          building: "Altgeld Hall",
          room: "314",
          location: "Altgeld Hall 314",
          instructors: "Smith, A"
        }
      },
      {
        title: "CHEM 102: General Chemistry I",
        description: "Fundamental principles of chemistry.",
        weekdays: ["Monday", "Wednesday", "Friday"],
        time: "12:00-12:50",
        courseData: {
          course: "CHEM 102",
          name: "General Chemistry I",
          description: "Chem...",
          credit: "3 hours",
          degree: "Physical Sciences",
          CRN: 11223,
          section: "E1",
          term: "1",
          type: "Lecture",
          start: "12:00:00 pm",
          end: "12:50:00 pm",
          days: "MWF",
          building: "Noyes Lab",
          room: "100",
          location: "Noyes Lab 100",
          instructors: "Marville, K"
        }
      }
    ]
  }
];

export default function Results() {
  const { state } = useAppStore();

  // Transform backend schedules to match ScheduleVisualizer format
  const displaySchedules = state.generatedSchedules.length > 0
    ? state.generatedSchedules.map((schedule, index) => {
        // Calculate total credit hours - only count each unique course once
        // (lectures and discussions for the same course share credit hours)
        const uniqueCourses = new Map<string, number>();
        schedule.schedule.forEach(section => {
          const courseCode = section.course; // e.g., "CS 128" or "MATH 314"
          if (!uniqueCourses.has(courseCode)) {
            const creditMatch = section.credit.match(/(\d+)/);
            const credits = creditMatch ? parseInt(creditMatch[1]) : 0;
            uniqueCourses.set(courseCode, credits);
          }
        });
        const creditHours = Array.from(uniqueCourses.values()).reduce((sum, credits) => sum + credits, 0);

        // Calculate match percentage (normalize score to 0-100)
        const matchPercentage = Math.min(100, Math.max(0, Math.round(schedule.score)));

        // Debug first schedule
        if (index === 0) {
          console.log('DEBUG: First schedule from backend:', schedule);
          console.log('DEBUG: Calculated score:', matchPercentage);
          console.log('DEBUG: Calculated credits:', creditHours);
          console.log('DEBUG: Number of courses:', schedule.schedule.length);
          console.log('DEBUG: All courses:', schedule.schedule.map(s => `${s.course} ${s.section} (CRN: ${s.CRN})`));
          if (schedule.schedule.length > 0) {
            console.log('DEBUG: First course time:', schedule.schedule[0].start, 'to', schedule.schedule[0].end);
            console.log('DEBUG: Formatted time:', `${formatTime(schedule.schedule[0].start)}-${formatTime(schedule.schedule[0].end)}`);
          }
        }

        const transformedCourses = schedule.schedule.map((section, sectionIdx) => {
          const weekdays = parseDaysToArray(section.days);
          const time = `${formatTime(section.start)}-${formatTime(section.end)}`;

          if (index === 0) {
            console.log(`DEBUG: Section ${sectionIdx} - ${section.course} ${section.section}:`, {
              rawDays: section.days,
              daysType: typeof section.days,
              daysValue: JSON.stringify(section.days),
              parsedWeekdays: weekdays,
              rawStart: section.start,
              rawEnd: section.end,
              formattedTime: time,
              hasValidDays: weekdays && weekdays.length > 0,
              hasValidTime: time && time.includes('-')
            });
          }

          return {
            title: `${section.course}: ${section.name}`,
            description: section.description,
            weekdays,
            time,
            courseData: section
          };
        });

        // Summary log for first schedule
        if (index === 0) {
          const lectureCount = transformedCourses.filter(c => c.courseData?.type?.toLowerCase().includes('lecture')).length;
          const discussionCount = transformedCourses.filter(c => c.courseData?.type?.toLowerCase().includes('discussion')).length;
          const labCount = transformedCourses.filter(c => c.courseData?.type?.toLowerCase().includes('lab')).length;
          const emptyDaysCount = transformedCourses.filter(c => !c.weekdays || c.weekdays.length === 0).length;

          console.log('DEBUG SUMMARY:', {
            totalSections: transformedCourses.length,
            lectures: lectureCount,
            discussions: discussionCount,
            labs: labCount,
            sectionsWithEmptyDays: emptyDaysCount
          });

          if (emptyDaysCount > 0) {
            console.warn(`WARNING: ${emptyDaysCount} section(s) have no weekdays and won't appear on calendar!`);
            transformedCourses.forEach((c, i) => {
              if (!c.weekdays || c.weekdays.length === 0) {
                console.warn(`  - ${c.title} (${c.courseData?.type} ${c.courseData?.section})`);
              }
            });
          }
        }

        return {
          id: String.fromCharCode(65 + index), // A, B, C, etc.
          matchPercentage,
          creditHours,
          courses: transformedCourses
        };
      })
    : MOCK_SCHEDULES; // Fallback to mock data if no schedules generated

  return (
    <main className="container mx-auto px-4 py-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="mb-8">
        <Link href="/">
          <Button variant="ghost" className="pl-0 hover:pl-2 transition-all mb-4 text-muted-foreground">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Planner
          </Button>
        </Link>
        <h1 className="text-3xl font-heading font-bold text-foreground">
          Recommended Schedules
        </h1>
        <p className="text-muted-foreground mt-2">
          {state.generatedSchedules.length > 0
            ? `Found ${state.generatedSchedules.length} schedule${state.generatedSchedules.length > 1 ? 's' : ''} based on your preferences for professor quality, timing, and location.`
            : "No schedules generated yet. Using sample data."}
        </p>
      </div>

      <div className="space-y-8">
        {displaySchedules.map((schedule) => (
          <ScheduleVisualizer
            key={schedule.id}
            id={schedule.id}
            matchPercentage={schedule.matchPercentage}
            creditHours={schedule.creditHours}
            courses={schedule.courses}
          />
        ))}
      </div>
    </main>
  );
}
