import { useState, useEffect, useCallback } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import slide1 from "@/assets/slide1_specialized_medicine.jpg";
import slide2 from "@/assets/slide2_health_priority.jpg";
import slide3 from "@/assets/slide3_exceptional_service.jpg";

interface AdCarouselProps {
  onAdClick: () => void;
}

const slides = [
  { id: 1, src: slide1, alt: "Specialized Medicine - Prevention is better than cure" },
  { id: 2, src: slide2, alt: "Your Health Is Our Priority" },
  { id: 3, src: slide3, alt: "Exceptional Service in Our Medical Practice" },
];

const AdCarousel = ({ onAdClick }: AdCarouselProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  const nextSlide = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % slides.length);
  }, []);

  const prevSlide = useCallback(() => {
    setCurrentIndex((prev) => (prev - 1 + slides.length) % slides.length);
  }, []);

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
    setIsAutoPlaying(false);
    setTimeout(() => setIsAutoPlaying(true), 5000);
  };

  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(nextSlide, 4000);
    return () => clearInterval(interval);
  }, [isAutoPlaying, nextSlide]);

  return (
    <div className="relative w-full max-w-5xl mx-auto group">
      {/* Main carousel container */}
      <div 
        className="relative overflow-hidden rounded-2xl shadow-card cursor-pointer transition-transform duration-300 hover:scale-[1.02]"
        onClick={onAdClick}
      >
        {/* Slides */}
        <div 
          className="flex transition-transform duration-700 ease-out"
          style={{ transform: `translateX(-${currentIndex * 100}%)` }}
        >
          {slides.map((slide) => (
            <div 
              key={slide.id} 
              className="w-full flex-shrink-0 relative"
            >
              <img
                src={slide.src}
                alt={slide.alt}
                className="w-full h-auto object-cover aspect-[16/7]"
              />
              {/* Hover overlay */}
              <div className="absolute inset-0 bg-primary/0 hover:bg-primary/10 transition-colors duration-300 flex items-center justify-center">
                <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-primary text-primary-foreground px-6 py-3 rounded-full font-display font-semibold shadow-glow">
                  Click to Book Appointment
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Gradient overlays */}
        <div className="absolute inset-0 bg-gradient-to-r from-background/5 via-transparent to-background/5 pointer-events-none" />
      </div>

      {/* Navigation arrows */}
      <button
        onClick={(e) => {
          e.stopPropagation();
          prevSlide();
        }}
        className="absolute left-4 top-1/2 -translate-y-1/2 bg-card/90 backdrop-blur-sm p-3 rounded-full shadow-soft opacity-0 group-hover:opacity-100 transition-all duration-300 hover:bg-card hover:shadow-glow"
        aria-label="Previous slide"
      >
        <ChevronLeft className="w-5 h-5 text-foreground" />
      </button>
      <button
        onClick={(e) => {
          e.stopPropagation();
          nextSlide();
        }}
        className="absolute right-4 top-1/2 -translate-y-1/2 bg-card/90 backdrop-blur-sm p-3 rounded-full shadow-soft opacity-0 group-hover:opacity-100 transition-all duration-300 hover:bg-card hover:shadow-glow"
        aria-label="Next slide"
      >
        <ChevronRight className="w-5 h-5 text-foreground" />
      </button>

      {/* Dots indicator */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={(e) => {
              e.stopPropagation();
              goToSlide(index);
            }}
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              index === currentIndex
                ? "bg-primary w-8 shadow-glow"
                : "bg-card/70 hover:bg-card"
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>

      {/* Click hint */}
      <p className="text-center mt-4 text-muted-foreground font-body text-sm animate-pulse-soft">
        ✨ Click on the ad to book your appointment
      </p>
    </div>
  );
};

export default AdCarousel;
